import re, glob, urllib.parse

html_files = glob.glob('**/*.html', recursive=True)
fixed_count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Match SVG data URIs - the SVG content is between the comma and the closing quote
    def fix_svg_href(m):
        prefix = m.group(1)  # href="data:image/svg+xml,
        svg_content = m.group(2)  # everything up to the closing quote
        quote = m.group(3)  # closing quote
        # URL-encode the SVG content
        encoded = urllib.parse.quote(svg_content, safe='')
        return prefix + encoded + quote
    
    # Pattern: href="data:image/svg+xml,..." or href='data:image/svg+xml,...'
    content = re.sub(
        r'(href=["\']data:image/svg\+xml,)(.*?)(["\'])',
        fix_svg_href,
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {filepath}')

print(f'\nTotal files fixed: {fixed_count}')
