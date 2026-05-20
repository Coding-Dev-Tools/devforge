import os, re, glob, sys

# Collect all internal HTML files
all_files = set()
for root, dirs, files in os.walk('.'):
    if '.git' in dirs:
        dirs.remove('.git')
    for f in files:
        if f.endswith('.html'):
            all_files.add(os.path.join(root, f))

# Extract paths relative to site root
actual_pages = set()
for fp in all_files:
    rel = os.path.relpath(fp, '.').replace(os.sep, '/')
    if rel.startswith('./'):
        rel = rel[2:]
    actual_pages.add(rel)

print(f"Actual HTML pages: {len(actual_pages)}")

# Now scan all HTML files for internal links
print("\n--- Broken link check ---")
broken = 0
checked = 0

for fp in sorted(all_files):
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Find all href links to .html files
    links = re.findall(r'href="([^"]+\.html)"', content)
    
    source_rel = os.path.relpath(fp, '.').replace(os.sep, '/')
    source_dir = os.path.dirname(source_rel)
    if source_dir == '.':
        source_dir = ''
    
    for link in links:
        checked += 1
        # Skip external links
        if link.startswith('http://') or link.startswith('https://'):
            continue
        # Skip anchors
        if link.startswith('#'):
            continue
        
        # Resolve relative path
        if link.startswith('../'):
            parts = source_dir.split('/') if source_dir else []
            up_count = link.count('../')
            resolved_parts = parts[:-up_count] if len(parts) >= up_count else []
            remaining = link[3*up_count:]
            resolved = '/'.join(resolved_parts + [remaining]) if resolved_parts else remaining
        elif link.startswith('./'):
            resolved = (source_dir + '/' + link[2:]) if source_dir else link[2:]
        else:
            resolved = (source_dir + '/' + link) if source_dir else link
        
        resolved = resolved.replace('//', '/')
        
        # Check if the target file exists (using OS-native paths)
        target_path = resolved.replace('/', os.sep)
        if not os.path.exists(target_path):
            print(f"  BROKEN: {source_rel} -> {link}")
            broken += 1
        elif target_path not in all_files and not os.path.isdir(target_path):
            # It exists on disk but wasn't in our walk - rare but worth noting
            pass

print(f"\nChecked {checked} links, found {broken} broken")

# Exit with error code for CI
if broken > 0:
    sys.exit(1)
