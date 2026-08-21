#!/usr/bin/env python3
"""Fix SRI hashes in all HTML files"""
import glob

FA_HASH = 'sha512-9xKTRVabjVeZmc+GUW8GgSmcREDunMM+Dt/GrzchfN8tkwHizc5RP4Ok/MXFFy5rIjJjzhndFScTceq5e6GvVQ=='
HLJS_CSS_HASH = 'sha512-hasIneQUHlh06VNBe7f6ZcHmeRTLIaQWFd43YriJ0UND19bvYRauxthDg8E4eVNPm9bRUhr5JGeqH7FRFXQu5g=='
HLJS_JS_HASH = 'sha512-6yoqbrcLAHDWAdQmiRlHG4+m0g/CT/V9AGyxabG8j7Jk8j3r3K6due7oqpiRMZqcYe9WM2gPcaNNxnl2ux+3tA=='

files = glob.glob('**/*.html', recursive=True)

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Fix Font Awesome hash
    if 'font-awesome/6.7.0' in content:
        import re
        content = re.sub(
            r'font-awesome/6\.7\.0/css/all\.min\.css" integrity="[^"]*"',
            f'font-awesome/6.7.0/css/all.min.css" integrity="{FA_HASH}"',
            content
        )

    # Fix Highlight.js CSS hash
    if 'highlight.js/11.10.0/styles' in content:
        import re
        content = re.sub(
            r'highlight\.js/11\.10\.0/styles/default\.min\.css" integrity="[^"]*"',
            f'highlight.js/11.10.0/styles/default.min.css" integrity="{HLJS_CSS_HASH}"',
            content
        )

    # Fix Highlight.js JS hash
    if 'highlight.js/11.10.0/highlight.min.js' in content:
        import re
        content = re.sub(
            r'highlight\.js/11\.10\.0/highlight\.min\.js" integrity="[^"]*"',
            f'highlight.js/11.10.0/highlight.min.js" integrity="{HLJS_JS_HASH}"',
            content
        )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'✅ Fixed: {filepath}')

print('Done!')
