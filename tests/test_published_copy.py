"""Audit the complete Pages artifact, with product-specific attribution.

Pinned evidence checked for this contract:
SchemaForge b6eecadd288589f073ae2ca59018455f9814bbf4:
  src/schemaforge/cli.py (_FORMATS), README.md (Supported Formats/Limitations)
DeadCode 272bfa8dd83b91aebeca96304404e7b64871c753:
  src/deadcode/scanner.py (regex patterns and four finding categories)
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings

ROOT = Path(__file__).resolve().parents[1]
BRANDS = re.compile(r"SchemaForge|DeadCode", re.I)
COMPETITORS = re.compile(r"\b(?:knip|ts-prune|ESLint)\b", re.I)
OTHER_PRODUCTS = re.compile(r"DataMorph|APIAuth|APIGhost|Envault|ConfigDrift|DeployDiff|json2sql|click-to-mcp|API Contract Guardian", re.I)


def product_scope(node):
    """Attribute table cells to their own column and copy to its nearest topic."""
    if node.name in {"td", "th"}:
        table = node.find_parent("table")
        row = node.find_parent("tr")
        if table is not None and row is not None:
            cells = row.find_all(["td", "th"], recursive=False)
            headers = table.find("tr").find_all(["td", "th"], recursive=False)
            index = next((i for i, cell in enumerate(cells) if cell is node), -1)
            if 0 <= index < len(headers):
                label = headers[index].get_text(" ", strip=True)
                match = BRANDS.search(label)
                if match:
                    return match.group().lower()
                if COMPETITORS.search(label):
                    return None
    text = node.get("content", "") if node.name == "meta" else node.get_text(" ", strip=True)
    match = BRANDS.search(text)
    if match:
        return match.group().lower()
    for heading in node.find_all_previous(["h1", "h2", "h3", "h4"]):
        label = heading.get_text(" ", strip=True)
        match = BRANDS.search(label)
        if match:
            return match.group().lower()
        if COMPETITORS.search(label) or OTHER_PRODUCTS.search(label) or re.match(r"Tool [2-9]:", label):
            return None
    title = node.find_previous("title")
    match = BRANDS.search(title.get_text() if title else "")
    return match.group().lower() if match else None


def copy_issues(text):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(text, "html.parser")
    issues = []
    for node in soup.find_all(["p", "li", "td", "th", "meta", "div", "span", "summary", "title", "h1", "h2", "h3", "h4", "text", "tspan"]):
        if node.name in {"div", "span"} and node.find(["p", "li", "td", "th", "h1", "h2", "h3", "div"]):
            continue
        copy = node.get("content", "") if node.name == "meta" else node.get_text(" ", strip=True)
        scope = product_scope(node)
        if scope == "schemaforge":
            if re.search(r"\b110\s+(?:(?:bidirectional|conversion|direction)\s+)*(?:paths|directions|pairs)", copy, re.I):
                issues.append(("schema-direction-count", copy))
            if re.search(r"\bzero(?:[- ]+information)?[- ]+loss\b", copy, re.I):
                issues.append(("schema-loss-guarantee", copy))
            format_list = re.search(r"(?:11|eleven)\s+(?:schema\s+|ORM\s+|supported\s+)?formats|convert between|define your schema", copy, re.I)
            if node.name == "td":
                table = node.find_parent("table")
                header = table.find(["th", "td"]).get_text(strip=True) if table else ""
                format_list = format_list or header == "Format"
            if format_list and re.search(r"\b(?:Protobuf|Avro|OpenAPI|YAML)\b", copy):
                issues.append(("schema-unsupported-format", copy))
            if format_list and "Alembic" in copy and re.search(r"bidirectional", copy, re.I) and not re.search(r"export[- ]only|export only|generator[- ]only", copy, re.I):
                issues.append(("schema-alembic-direction", copy))
            if re.search(r"full[^.!?]*\brelationships\b", copy, re.I):
                issues.append(("schema-relationship-preservation", copy))
        elif scope == "deadcode":
            qualified = re.sub(r"\b(?:no|without|does not use|does not build)\s+(?:an?\s+)?(?:AST(?:\s+or\s+tree-sitter)?|tree-sitter|abstract syntax tree)", "", copy, flags=re.I)
            if re.search(r"\bAST\b|abstract syntax tree|tree[- ]sitter|compiler(?:'s)?\s+API", qualified, re.I):
                issues.append(("deadcode-implementation", copy))
    return issues


@pytest.fixture(scope="module")
def published_artifact(tmp_path_factory):
    output = tmp_path_factory.mktemp("published-copy")
    subprocess.run([sys.executable, str(ROOT / "scripts/build_pages_artifact.py"), "--source", str(ROOT), "--output", str(output)], check=True)
    return output


def test_all_published_copy_matches_pinned_implementation(published_artifact):
    issues = {}
    for path in sorted(published_artifact.rglob("*")):
        if path.is_file():
            found = copy_issues(path.read_text(encoding="utf-8-sig"))
            if found:
                issues[path.relative_to(published_artifact).as_posix()] = found
    assert not issues, issues


@pytest.mark.parametrize("html,kind", [
    ('<h3>SchemaForge</h3><p>11 formats: Prisma, Avro, Protobuf, OpenAPI.</p>', "schema-unsupported-format"),
    ('<p>SchemaForge supports 110 conversion paths.</p>', "schema-direction-count"),
    ('<h2>SchemaForge</h2><p>Define your schema in Python, TypeScript or YAML.</p>', "schema-unsupported-format"),
    ('<h3>DeadCode</h3><p>Full TypeScript compiler API.</p>', "deadcode-implementation"),
    ('<title>DeadCode</title><meta name="description" content="AST parsing">', "deadcode-implementation"),
])
def test_known_omissions_are_detected_without_filename_gates(html, kind):
    assert kind in {issue[0] for issue in copy_issues(html)}


def test_accurate_competitor_and_conditional_claims_are_preserved():
    html = '<h2>DeadCode vs knip</h2><table><tr><th>Feature</th><th>DeadCode</th><th>knip</th></tr><tr><td>Scanner</td><td>Regex-based</td><td>TypeScript compiler API</td></tr></table>'
    html += '<h2>SchemaForge</h2><p>If the roundtrip produces the same schema, the conversion is lossless.</p>'
    html += '<h2>DataMorph</h2><p>Convert between CSV, JSON, Avro and Protobuf.</p>'
    assert not copy_issues(html)
