# Modernization Scripts

Utility scripts created during the site modernization process.

## Scripts

### `modernize-article.py`

Modernizes blog post HTML files to work with the new architecture.

**Usage:**
```bash
python3 .claude/scripts/modernize-article.py path/to/blog-post/index.html
```

**What it does:**
- Removes Bootstrap CSS and JS
- Removes jQuery
- Updates navbar HTML to modern version
- Adds preconnect hints
- Updates Font Awesome 4.5 → 6.7
- Updates Highlight.js 9.8 → 11.10
- Fixes all HTTP links to HTTPS
- Adds mobile menu JavaScript

**Use when:** Extracting new blog posts from the old master branch.

---

### `fix-sri-hashes.py`

Fixes SRI (Subresource Integrity) hashes for external CDN resources.

**Usage:**
```bash
python3 .claude/scripts/fix-sri-hashes.py
```

**What it does:**
- Updates Font Awesome CSS integrity hash
- Updates Highlight.js CSS integrity hash
- Updates Highlight.js JS integrity hash
- Scans all `*.html` files recursively

**Use when:** 
- Updating CDN library versions
- SRI hash mismatches causing browser security blocks
- After manual HTML edits that might have corrupted hashes

---

### `convert-to-fontawesome.py`

Converts glyphicon classes to proper Font Awesome 6 classes.

**Usage:**
```bash
python3 .claude/scripts/convert-to-fontawesome.py
```

**What it does:**
- Converts `glyphicon glyphicon-hand-right` → `fa-solid fa-hand-point-right`
- Converts `glyphicon glyphicon-time` → `fa-regular fa-clock`
- Converts `glyphicon glyphicon-film` → `fa-solid fa-film`
- Converts `glyphicon glyphicon-blackboard` → `fa-solid fa-chalkboard`
- Converts `glyphicon glyphicon-arrow-right` → `fa-solid fa-arrow-right`
- Scans all `*.html` files (except slides directory)

**Use when:** 
- Migrating from Bootstrap Glyphicons to Font Awesome
- Cleaning up CSS shims in favor of proper icon classes

**Note:** After running, remove the CSS shims from `css/site.css`.

---

## Notes

These scripts were created during the modernization of the site from a Metalsmith/Jade build system to static HTML with modern CSS.

See `CLAUDE.md` for full project context and `CHANGELOG.md` for modernization history.
