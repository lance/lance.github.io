#!/usr/bin/env python3
"""
Convert glyphicon classes to proper Font Awesome 6 classes
"""
import glob
import re

# Mapping of glyphicon classes to Font Awesome classes
ICON_MAPPINGS = {
    'glyphicon glyphicon-hand-right': 'fa-solid fa-hand-point-right',
    'glyphicon glyphicon-time': 'fa-regular fa-clock',
    'glyphicon glyphicon-film': 'fa-solid fa-film',
    'glyphicon glyphicon-blackboard': 'fa-solid fa-chalkboard',
    'glyphicon glyphicon-arrow-right': 'fa-solid fa-arrow-right',
}

def convert_file(filepath):
    """Convert glyphicon classes to Font Awesome in a single file"""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Replace each glyphicon class with Font Awesome equivalent
    for old_class, new_class in ICON_MAPPINGS.items():
        # Handle both span and i tags
        content = re.sub(
            rf'<span class="{re.escape(old_class)}">',
            f'<i class="{new_class}"></i><span>',
            content
        )
        # Also handle self-closing spans
        content = re.sub(
            rf'<span class="{re.escape(old_class)}">&nbsp;</span>',
            f'<i class="{new_class}"></i> ',
            content
        )
        # Handle spans without &nbsp;
        content = re.sub(
            rf'<span class="{re.escape(old_class)}"></span>',
            f'<i class="{new_class}"></i>',
            content
        )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# Find all HTML files
html_files = glob.glob('**/*.html', recursive=True)
html_files = [f for f in html_files if not f.startswith('slides/')]  # Skip slides

converted = []
for filepath in html_files:
    if convert_file(filepath):
        converted.append(filepath)
        print(f'✅ Converted: {filepath}')

print(f'\n🎉 Converted {len(converted)} files to Font Awesome 6!')
print('\nNext step: Remove CSS shims from css/site.css')
