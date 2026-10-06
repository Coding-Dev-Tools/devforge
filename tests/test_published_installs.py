"""Audit owned-tool install requirements in the complete production artifact.

The fixture records the distribution names, console scripts and extras from
each owned repository's pyproject.toml at its recorded commit. Source URLs are
repository names, not distribution names. These checks enforce the documented
GitHub installation route; they do not infer current PyPI ownership/availability.
"""

import json
import os
import re
import shlex
import subprocess
import warnings
from importlib import metadata
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

from test_published_copy import published_artifact

ROOT = Path(__file__).resolve().parents[1]
TOOLS = json.loads((ROOT / "tests/fixtures/tool_install_metadata.json").read_text())
# Formula names checked against homebrew-tap a4292def4277cfc4e99727720435ae9c20cb9a20.
FORMULAS = set(TOOLS) - {"json2sql"} | {"json2sql-cli"}
OWNED_NAMES = set(TOOLS) | {tool["distribution"] for tool in TOOLS.values()} | {
    "envault-secrets", "apighost-cli",
}
VCS = re.compile(r"git\+https://github\.com/Coding-Dev-Tools/[^\s\"'<>;,]+")


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def source_requirement_issues(requirement):
    issues = []
    named = re.fullmatch(r"([\w.-]+)(?:\[([^\]]+)\])?\s*@\s*(git\+.*)", requirement)
    url = named[3] if named else requirement
    if not url.startswith("git+https://github.com/Coding-Dev-Tools/"):
        if named and normalize(named[1]) in {normalize(name) for name in OWNED_NAMES}:
            issues.append(("incomplete-owned-source", requirement))
        return issues
    parsed = urlsplit(url[4:])
    match = re.fullmatch(r"/Coding-Dev-Tools/([a-z0-9-]+)\.git(?:@[^/\s]+)?", parsed.path)
    if match is None or match[1] not in TOOLS:
        return [("owned-repository-url", requirement)]
    tool = TOOLS[match[1]]
    if named:
        if normalize(named[1]) != normalize(tool["distribution"]):
            issues.append(("distribution-name", requirement))
        if named[2] and not set(named[2].split(",")) <= set(tool["extras"]):
            issues.append(("undeclared-extra", requirement))
    return issues


def install_commands(text):
    """Read shell continuations and folded YAML requirement-only continuations."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.search(r"\b(?:pip(?:3)?|pipx|uv pip)\s+install\s*(.*)", line)
        if not match:
            continue
        command = match[1].strip()
        cursor = index + 1
        while cursor < len(lines):
            continuation = command.endswith("\\")
            next_line = lines[cursor].strip()
            folded = next_line.startswith("git+https://")
            if not continuation and not folded:
                break
            command = command.removesuffix("\\").rstrip() + " " + next_line
            cursor += 1
        yield command


def install_issues(html):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(html, "html.parser")
    issues = []
    # Inspect every rendered source URL, including CTAs outside code blocks.
    for requirement in VCS.findall(soup.get_text(" ")):
        issues.extend(source_requirement_issues(requirement.rstrip(").")))
    for br in soup.find_all("br"):
        br.replace_with("\n")
    nodes = soup.find_all("code")
    nodes += [node for node in soup.find_all("p") if not node.find("code")]
    nodes += soup.select("div.cmd-block")
    nodes += soup.find_all("svg")
    for node in nodes:
        # SVG terminal commands can span adjacent text elements.
        rendered = node.get_text("\n") if node.name == "svg" else node.get_text()
        for command in install_commands(rendered):
            try:
                requirements = shlex.split(command, comments=True)
            except ValueError:
                issues.append(("install-syntax", command))
                continue
            for requirement in requirements:
                if requirement in {"·", "&&", ";", "||", "|"}:
                    break
                issues.extend(source_requirement_issues(requirement))
                name = re.split(r"[\[<>=!~]", requirement, maxsplit=1)[0]
                if "@" not in requirement and normalize(name) in {normalize(name) for name in OWNED_NAMES}:
                    issues.append(("owned-tool-without-source", requirement))
        for match in re.finditer(r"\bbrew\s+install\s+([^\n]+)", rendered):
            for argument in shlex.split(match[1], comments=True):
                formula = argument.rsplit("/", 1)[-1]
                if formula in TOOLS and formula not in FORMULAS:
                    issues.append(("owned-formula-name", formula))
    return sorted(set(issues))


def test_all_published_installs_use_owned_sources_and_metadata(published_artifact):
    issues = {}
    for path in sorted(published_artifact.rglob("*")):
        if path.is_file():
            found = install_issues(path.read_text(encoding="utf-8-sig"))
            if found:
                issues[path.relative_to(published_artifact).as_posix()] = found
    assert not issues, issues


def test_roundup_homebrew_suite_installs_all_eleven_formula_names(published_artifact):
    page = published_artifact / "blog/10-open-source-cli-tools-ai-development.html"
    soup = BeautifulSoup(page.read_text(), "html.parser")
    block = next(node.get_text() for node in soup.find_all("code") if "brew tap" in node.get_text())
    line = next(line for line in block.splitlines() if line.startswith("brew install "))
    assert set(shlex.split(line)[2:]) == FORMULAS


@pytest.mark.parametrize("html,kind", [
    ('<pre><code>pip install git+https://github.com/Coding-Dev-Tools/json2sql.git-cli</code></pre>', "owned-repository-url"),
    ('<p>pip install git+https://github.com/Coding-Dev-Tools/envault.git-secrets · Try it</p>', "owned-repository-url"),
    ('<code>pip install "datamorph[parquet] @ git+https://github.com/Coding-Dev-Tools/datamorph.git"</code>', "distribution-name"),
    ('<code>pip install "datamorph-cli[missing] @ git+https://github.com/Coding-Dev-Tools/datamorph.git"</code>', "undeclared-extra"),
    ('<code>pip install "datamorph[all] @ git+https://..."</code>', "incomplete-owned-source"),
    ('<code>pip install \\\n envault-secrets \\\n json2sql-cli</code>', "owned-tool-without-source"),
    ('<code>run: >-\n pip install\n git+https://github.com/Coding-Dev-Tools/apighost.git-cli</code>', "owned-repository-url"),
    ('<code>brew install json2sql</code>', "owned-formula-name"),
])
def test_install_audit_rejects_known_failure_patterns(html, kind):
    assert kind in {issue[0] for issue in install_issues(html)}


@pytest.mark.parametrize("requirement", [
    "git+https://github.com/Coding-Dev-Tools/json2sql.git",
    "git+https://github.com/Coding-Dev-Tools/envault.git@f68571b592e028250ec06d184e4ab53603d38a0f",
    "datamorph-cli[parquet,avro] @ git+https://github.com/Coding-Dev-Tools/datamorph.git",
    "click-to-mcp[http] @ git+https://github.com/Coding-Dev-Tools/click-to-mcp.git",
])
def test_install_audit_accepts_valid_sources_revisions_and_extras(requirement):
    assert not source_requirement_issues(requirement)


def test_install_audit_preserves_third_party_and_local_installs():
    assert not install_issues('<code>pip install pandas pyarrow pytest\npip install -e ".[dev]"\npip install dist/*.whl</code>')


def test_install_audit_preserves_html_breaks_and_svg_terminal_continuations():
    assert not install_issues('<div class="cmd-block">$ pip install git+https://github.com/Coding-Dev-Tools/json2sql.git<br>$ json2sql --help</div>')
    assert not install_issues('<svg><text>$ pip install \\</text><text>git+https://github.com/Coding-Dev-Tools/click-to-mcp.git</text></svg>')
    assert not install_issues('<p>pip install git+https://github.com/Coding-Dev-Tools/envault.git · rh-envault --help</p>')
    assert not install_issues('<code>brew install Coding-Dev-Tools/homebrew-tap/json2sql-cli apiauth</code>')


@pytest.mark.skipif(os.environ.get("DEVFORGE_UPSTREAM_SMOKE") != "1", reason="run in the CLI Example Smoke job")
def test_installed_owned_distributions_expose_the_pinned_console_scripts(tmp_path):
    for repository, tool in TOOLS.items():
        installed = metadata.distribution(tool["distribution"])
        scripts = {entry.name for entry in installed.entry_points if entry.group == "console_scripts"}
        assert set(tool["scripts"]) <= scripts, repository
        assert set(tool["extras"]) <= set(installed.metadata.get_all("Provides-Extra") or []), repository
        direct = json.loads(installed.read_text("direct_url.json"))
        assert direct["url"] == f"https://github.com/Coding-Dev-Tools/{repository}.git", repository
        for executable in tool["scripts"]:
            result = subprocess.run([executable, "--help"], cwd=tmp_path, capture_output=True, text=True, timeout=60)
            assert result.returncode == 0, f"{repository}: {result.stdout}{result.stderr}"
