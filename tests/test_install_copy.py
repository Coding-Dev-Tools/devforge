"""Keep rendered marketing commands consistent with the tools they promise."""

import re
import shlex
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "api-contract-guardian",
    "json2sql",
    "deploydiff",
    "configdrift",
    "apiauth",
    "apighost",
    "envault",
    "schemaforge",
    "datamorph",
    "click-to-mcp",
    "deadcode",
}


class CodeBlocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "code":
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == "code" and self.current is not None:
            self.blocks.append("".join(self.current))
            self.current = None


def code_blocks(filename):
    parser = CodeBlocks()
    parser.feed((ROOT / filename).read_text(encoding="utf-8-sig"))
    return parser.blocks


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
        "docs.html",
        "quickstart.html",
        "blog/autonomous-ai-experiment.html",
    ],
)
def test_full_suite_command_installs_each_tool_repository(page):
    commands = []
    for block in code_blocks(page):
        # A literal newline must terminate the command. Bash continuations cannot
        # be pasted into the Windows shells advertised by these pages.
        commands.extend(block.splitlines())
    for command in commands:
        if command.strip().startswith("pip install "):
            arguments = shlex.split(command)
            installed = {
                match.group(1)
                for argument in arguments[2:]
                if (
                    match := re.fullmatch(
                        r"git\+https://github.com/Coding-Dev-Tools/([a-z0-9-]+)\.git",
                        argument,
                    )
                )
            }
            if installed == TOOLS:
                break
    else:
        pytest.fail(f"{page}: suite command does not install all eleven tools")

    text = (ROOT / page).read_text(encoding="utf-8-sig")
    assert "pip install git+https://github.com/Coding-Dev-Tools/devforge.git" not in text
    assert "pip install devforge-tools" not in text


def test_ci_example_installs_the_four_commands_it_runs():
    example = next(block for block in code_blocks("docs.html") if "CI Safety Net" in block)
    installed = set(re.findall(r"Coding-Dev-Tools/([a-z0-9-]+)\.git", example))
    assert {"api-contract-guardian", "json2sql", "deploydiff", "configdrift"} <= installed


def test_envault_cta_preserves_the_executable_after_install():
    text = (ROOT / "blog/envault-serve-http-api-secrets.html").read_text(encoding="utf-8")
    assert "envault.git &middot; rh-envault serve --port 8080 --api-key" in text
    assert "envault.git serve" not in text
    # The published HTTP handler accepts X-API-Key for --api-key. The article
    # must not promise a token derived automatically from the encryption key.
    assert "X-API-Key:" in text
    assert "SHA-256" not in text
    assert "Authorization: Bearer" not in text


def test_click_to_mcp_does_not_claim_git_install_is_on_pypi():
    comparison = (ROOT / "alternatives.html").read_text(encoding="utf-8")
    cell = re.search(r"<td>PyPI package</td>\s*<td[^>]*>(.*?)</td>", comparison)
    assert cell is not None
    assert "Coming soon" in cell.group(1)
    assert "GitHub" in cell.group(1)

    article = (ROOT / "blog/click-to-mcp-intro.html").read_text(encoding="utf-8")
    assert "already on PyPI" not in article
    assert "coming soon; install from GitHub" in article
