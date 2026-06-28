import glob

# Recolor all pages that still have indigo, and add focus rings
accent = [
    ('#6366f1', '#10b981'),
    ('#5558e6', '#059669'),
    ('#a78bfa', '#6ee7b7'),
    ('#4f46e5', '#047857'),
    ('rgba(99,102,241,', 'rgba(16,185,129,'),
    ('rgba(99, 102, 241,', 'rgba(16, 185, 129,'),
    ('rgba(168,85,247,', 'rgba(110,231,183,'),
    ('rgba(139,92,246,', 'rgba(52,211,153,'),
]
gradient = [
    ('#6366f1, #a78bfa', '#10b981, #34d399'),
]

focus_css = '    a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px dashed #10b981; outline-offset: 3px; border-radius: 2px; }'

pages = (glob.glob('*.html') + glob.glob('blog/*.html'))

for fpath in sorted(pages):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Recolor
    for old, new in accent:
        content = content.replace(old, new)
    for old, new in gradient:
        content = content.replace(old, new)

    # Add focus ring CSS if missing
    if 'focus-visible' not in content and '/* Navigation */' in content:
        content = content.replace(
            '    body { font-family: \'Inter\'',
            '    /* Focus rings */\n    a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px dashed #10b981; outline-offset: 3px; border-radius: 2px; }\n\n    body { font-family: \'Inter\''
        )

    if content != original and fpath != 'index.html':  # index already done
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done')
