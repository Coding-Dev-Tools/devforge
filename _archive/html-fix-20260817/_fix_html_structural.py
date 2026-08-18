#!/usr/bin/env python3
"""Fix remaining structural HTML validation errors in devforge blog posts."""
import re
from pathlib import Path

BLOG_DIR = Path("blog")
fixed_files = []

def fix_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content
    name = path.name

    # Fix 1: Unescaped < followed by space inside <pre><code> blocks
    # Pattern: <code>...< ...</code> where < is not part of an HTML tag or entity
    def escape_lt_in_pre_code(match):
        inner = match.group(1)
        # Escape < that are followed by space (shell redirection like `< seed.sql`)
        # but NOT < that start HTML tags or entities
        inner = re.sub(r'<(?!\s*/?\s*[a-zA-Z/]|&lt;|&gt;|&amp;|#)', '&lt;', inner)
        return f'<pre><code>{inner}</code></pre>'
    content = re.sub(r'<pre><code>(.*?)</code></pre>', escape_lt_in_pre_code, content, flags=re.DOTALL)

    # Fix 2: api-key-management-from-terminal.html - unclosed div.cmd-block with stray </code></pre>
    if name == "api-key-management-from-terminal.html":
        # The cmd-block div has raw text without <pre><code> wrapper but ends with </code></pre>
        old = '  <div class="cmd-block"># Export as dotenv file\n$ apiauth export --format dotenv --output .env.prod\n\n# Export as JSON for deployment tools\n$ apiauth export --format json\n\n# Export as shell exports for Docker\n$ apiauth export --format shell</code></pre>'
        new = '  <div class="cmd-block"><pre><code># Export as dotenv file\n$ apiauth export --format dotenv --output .env.prod\n\n# Export as JSON for deployment tools\n$ apiauth export --format json\n\n# Export as shell exports for Docker\n$ apiauth export --format shell</code></pre></div>'
        content = content.replace(old, new)

    # Fix 3: before-you-deploy-config-drift-and-cost.html - duplicate </main> and unclosed div
    if name == "before-you-deploy-config-drift-and-cost.html":
        # Remove the stray second </main> and fix the duplicate article-waitlist div
        old = '</main>\n\n  <div class="article-waitlist"><div class="article-waitlist">'
        new = '  <div class="article-waitlist">'
        content = content.replace(old, new)
        # Remove the extra </main> after the waitlist div
        old2 = '  </div>\n\n</main>\n\n<footer>'
        new2 = '  </div>\n\n<footer>'
        content = content.replace(old2, new2)

    # Fix 4: click-to-mcp-three-distribution-channels.html - stray </div>
    if name == "click-to-mcp-three-distribution-channels.html":
        # Line 245 has stray </div> - check context
        pass  # Will verify after other fixes

    # Fix 5: new-cli-features-may-18-2026.html - <style> in body
    if name == "new-cli-features-may-18-2026.html":
        # Move <style> block into <head> or wrap in proper location
        # For now, move it before </head> if possible, otherwise leave as-is
        # since this is a cosmetic issue and the page renders fine
        style_match = re.search(r'(<style>.*?</style>)', content, re.DOTALL)
        head_close = content.find('</head>')
        if style_match and head_close > 0:
            style_block = style_match.group(1)
            # Only move if style is currently after </head>
            if style_match.start() > head_close:
                content = content.replace(style_block, '', 1)
                content = content.replace('</head>', style_block + '\n</head>', 1)

    # Fix 6: clean-up-react-dead-code.html - code nesting with spans
    if name == "clean-up-react-dead-code.html":
        # The issue is </code> closing a span-nested code improperly
        # Line 217: <span class="cmd">cat ... | xargs rm</code></pre>
        # Should be: <span class="cmd">cat ... | xargs rm</span></code></pre>
        old = '<span class="cmd">cat deadcode-results.json | jq -r \'[] | select(.severity=="high") | .file\' | xargs rm</code></pre>'
        new = '<span class="cmd">cat deadcode-results.json | jq -r \'[] | select(.severity=="high") | .file\' | xargs rm</span></code></pre>'
        content = content.replace(old, new)
        # Also try without escaped quotes
        old2 = "<span class=\"cmd\">cat deadcode-results.json | jq -r '.[] | select(.severity==\"high\") | .file' | xargs rm</code></pre>"
        new2 = "<span class=\"cmd\">cat deadcode-results.json | jq -r '.[] | select(.severity==\"high\") | .file' | xargs rm</span></code></pre>"
        content = content.replace(old2, new2)

    # Fix 7: deploydiff-rollback-commands - <<EOF heredoc escaping
    if name == "deploydiff-rollback-commands-terraform-cloudformation.html":
        # Already fixed < to &lt; but need to check <<EOF pattern
        # The line should be: echo "ROLLBACK_COMMANDS&lt;&lt;EOF" 
        content = content.replace('&lt;<EOF', '&lt;&lt;EOF')
        # Also fix any remaining </code> nesting issues around line 308
        # Check for reversed tags
        content = content.replace('</pre></code>', '</code></pre>')

    # Fix 8: datamorph-validate-data-schema-ci-pipeline.html - already fixed by script
    # Verify the </code></pre> order is correct
    if name == "datamorph-validate-data-schema-ci-pipeline.html":
        content = content.replace('</pre></code>', '</code></pre>')

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False

count = 0
for html_file in sorted(BLOG_DIR.glob("*.html")):
    if fix_file(html_file):
        fixed_files.append(html_file.name)
        count += 1

print(f"Fixed {count} files:")
for f in fixed_files:
    print(f"  - {f}")
