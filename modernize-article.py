#!/usr/bin/env python3
"""
Modernize blog post HTML files to work with new architecture
"""
import sys
import re

def modernize_article(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Save backup
    with open(filepath + '.bak', 'w') as f:
        f.write(content)

    # Remove Bootstrap CSS
    content = re.sub(r'  <link rel="stylesheet"[^>]*bootstrap[^>]*>\n', '', content)

    # Update Font Awesome
    content = content.replace(
        'https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.0/css/all.min.css" integrity="sha512-9xKTRVabjVeZmc+GUW8GgSmcREDunMM+Dt/GrzchfN8tkwHizc5RP4Ok/MXFFy5rIjrKTfjrBU0gP8lhN2Lxqw==" crossorigin="anonymous" referrerpolicy="no-referrer"'
    )

    # Update Highlight.js CSS
    content = content.replace(
        'http://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.8.0/styles/default.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/styles/default.min.css" integrity="sha512-hasIneQUHlh06VNBe7f6ZcHmeRTLIaQWFd43YriJ0UND19bvYRauxthDg8E4eVNPm9bRUhr5JGeqH7FRFXQu5g==" crossorigin="anonymous" referrerpolicy="no-referrer"'
    )

    # Update Google Fonts
    content = content.replace(
        'https://fonts.googleapis.com/css?family=Open+Sans:400,300,600',
        'https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600&display=swap'
    )

    # Add preconnect hints if not present
    if 'preconnect' not in content:
        preconnect = '''  <!-- Preconnect to external resources for better performance -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdnjs.cloudflare.com">

'''
        content = content.replace('<link rel="stylesheet"', preconnect + '<link rel="stylesheet"', 1)

    # Update navbar HTML - old Bootstrap to new modern navbar
    old_navbar = r'<nav class="navbar navbar-default navbar-fixed-top">.*?</nav>'
    new_navbar = '''<nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a class="navbar-brand" href="/">Lance Ball</a>
      <button class="navbar-toggle" type="button" aria-expanded="false" aria-controls="navbar" aria-label="Toggle navigation">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <div class="navbar-collapse" id="navbar">
        <ul class="nav">
          <li><a href="https://github.com/lance">GitHub</a></li>
          <li><a href="https://twitter.com/lanceball">Twitter</a></li>
          <li><a href="https://www.linkedin.com/in/lanceball">LinkedIn</a></li>
          <li><a href="https://tumblr.lanceball.com">Tumblr</a></li>
        </ul>
      </div>
    </div>
  </nav>'''
    content = re.sub(old_navbar, new_navbar, content, flags=re.DOTALL)

    # Fix HTTP links to HTTPS
    content = content.replace('http://twitter.com', 'https://twitter.com')
    content = content.replace('http://www.linkedin.com', 'https://www.linkedin.com')
    content = content.replace('http://tumblr.lanceball.com', 'https://tumblr.lanceball.com')
    content = content.replace('http://redhat.com', 'https://redhat.com')

    # Remove jQuery and Bootstrap JS
    content = re.sub(r'  <script src="https://ajax\.googleapis\.com/ajax/libs/jquery[^>]*></script>\n', '', content)
    content = re.sub(r'  <script src="/lib/bootstrap/js/bootstrap\.min\.js"></script>\n', '', content)

    # Update Highlight.js script
    content = content.replace(
        'http://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.8.0/highlight.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/highlight.min.js" integrity="sha512-6yoqbrcLAHDWAdQmiRlHG4+m0g/CT/V9AGyxabG8j7Jk8j3r3K6due7oqpiRMZqcYe9WM2gPcaNNxnl2ux+3tA==" crossorigin="anonymous" referrerpolicy="no-referrer"'
    )
    content = content.replace('hljs.initHighlightingOnLoad()', 'hljs.highlightAll()')

    # Fix Google Analytics
    content = content.replace("'//www.google-analytics.com/analytics.js'", "'https://www.google-analytics.com/analytics.js'")
    content = content.replace("'script', '//www.google-analytics.com/analytics.js'", "'script', 'https://www.google-analytics.com/analytics.js'")

    # Add mobile menu JavaScript if not present
    if 'navbar-toggle' in content and 'Mobile menu toggle' not in content:
        mobile_js = '''  <script>
    // Mobile menu toggle
    document.addEventListener('DOMContentLoaded', function() {
      const toggle = document.querySelector('.navbar-toggle');
      const menu = document.querySelector('.navbar-collapse');

      if (toggle && menu) {
        toggle.addEventListener('click', function() {
          menu.classList.toggle('show');
          const expanded = menu.classList.contains('show');
          toggle.setAttribute('aria-expanded', expanded);
        });
      }
    });

    // Google Analytics'''
        content = content.replace('    // Google Analytics', mobile_js)
        # Also need to fix the script structure
        content = re.sub(r'  <script>\n    \(function\(i', '''  <script>
    // Google Analytics
    (function(i''', content)

    # Write updated content
    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✅ Modernized {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 modernize-article.py <filepath>")
        sys.exit(1)

    modernize_article(sys.argv[1])
