#!/usr/bin/env python3
"""Fix systematic HTML validation errors in devforge blog posts."""
import os
import re
from pathlib import Path

BLOG_DIR = Path("blog")
fixed_files = []

def fix_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content
    
    # Fix 1: Reversed closing tags </pre></code> -> </code></pre>
    content = content.replace("</pre></code>", "</code></pre>")
    
    # Fix 2: Unescaped < inside <code> blocks (but not HTML tags)
    # Match < followed by space or common shell operators inside code contexts
    # Only escape < that are NOT part of HTML tags (no / or letter immediately after)
    def escape_lt_in_code(match):
        inner = match.group(1)
        # Escape bare < that aren't already &lt; and aren't HTML tags
        inner = re.sub(r'<(?!\s*/?\s*[a-zA-Z]|&lt;|\s)', '&lt;', inner)
        return f"<code>{inner}</code>"
    
    content = re.sub(r'<code>(.*?)</code>', escape_lt_in_code, content, flags=re.DOTALL)
    
    # Fix 3: Stray </ol> that should be </ul> (when preceded by <ul>)
    # Look for <ul>...<li>...</li>...</ol> pattern
    content = re.sub(
        r'(<ul[^>]*>.*?</li>\s*)</ol>',
        r'\1</ul>',
        content,
        flags=re.DOTALL
    )
    
    # Fix 4: Missing </div> before </main> - add closing div if unclosed
    # This is tricky; we'll handle specific known files
    
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False

# Process all HTML files in blog/
count = 0
for html_file in sorted(BLOG_DIR.glob("*.html")):
    if fix_file(html_file):
        fixed_files.append(html_file.name)
        count += 1

print(f"Fixed {count} files:")
for f in fixed_files:
    print(f"  - {f}")
