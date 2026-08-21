# Modernization Branch

This branch contains the compiled HTML output from the `master` branch, extracted and prettified for direct editing.

## What Changed

Instead of using the Metalsmith build system with Jade/Pug templates, this branch works directly with static HTML files. This simplifies everything:

- ✅ No build step required
- ✅ Zero npm dependencies (our server is pure Node.js)
- ✅ Direct HTML/CSS editing
- ✅ Easier to modernize incrementally
- ✅ All old build system files removed for clarity

## Directory Structure

```
.
├── index.html              # Main homepage (prettified from master)
├── css/
│   └── site.css           # Custom site styles
├── lib/
│   └── bootstrap/         # Bootstrap 3 files (to be modernized/removed)
├── words/
│   └── 2017/05/17/       # Blog post example
│       └── riviera-dev-2017/
│           └── index.html
└── serve-static.js        # Simple dev server
```

## Development Workflow

### Serve Locally

```bash
npm start
# or
node serve-static.js
```

Then visit http://localhost:8080

**Note:** Do NOT use the old `./serve.sh` - it's been removed. That was the old Metalsmith build system.

### Modernization Plan

The detailed modernization plan is available in the planning conversation. Key goals:

1. **Remove Bootstrap & jQuery** - Replace with modern custom CSS
2. **Modernize CSS** - Use CSS Grid, Flexbox, CSS Variables
3. **Add Dark Mode** - System preference support
4. **Fix Security** - HTTPS for all external resources
5. **Improve Accessibility** - Semantic HTML, ARIA labels, keyboard navigation
6. **Update Icons** - Replace Glyphicons with Font Awesome 6 or SVG

### Next Steps

Start with Phase 1 of the modernization plan:
- Fix HTTP/HTTPS mixed content
- Update external dependencies (Highlight.js, Font Awesome)
- Modernize font loading

## Files Currently Available

- `index.html` - Main homepage with all sections
- `css/site.css` - Custom styles (from develop branch)
- `lib/bootstrap/` - Bootstrap 3 files (will be removed)
- `words/2017/05/17/riviera-dev-2017/index.html` - Sample blog post

## Original Build System

The original Metalsmith/Jade setup is still on the `develop` branch. This branch (`modernization`) is a clean slate for working with static HTML.
