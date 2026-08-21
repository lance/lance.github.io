# Project: lanceball.com - Static Site Modernization

## Overview

Personal website and blog for Lance Ball. This is the **modernization branch** where we're converting from a Metalsmith/Jade build system to simple static HTML with modern CSS.

## Branch Strategy

- **`develop`** - Original Metalsmith/Jade build system (preserved)
- **`master`** - Compiled HTML output from develop branch
- **`modernization`** - THIS BRANCH - Static HTML being modernized (no build system)

## Current Status

We're modernizing the site in phases. The site now uses static HTML files with modern CSS.

### ✅ Completed Phases

**Phase 1: HTTPS & Dependencies** ✅
- All external resources use HTTPS with SRI integrity hashes
- Updated Font Awesome 4.5.0 → 6.7.0
- Updated Highlight.js 9.8.0 → 11.10.0
- Modern Google Fonts API with preconnect hints

**Phase 2: CSS Modernization** ✅
- Complete CSS rewrite with CSS Custom Properties (variables)
- Dark mode support via `@media (prefers-color-scheme: dark)`
- Modern layout with Flexbox
- Improved accessibility (focus states, reduced motion support)
- Responsive design with mobile breakpoints

### 🚧 Pending Phases

**Phase 3: Remove Bootstrap & jQuery** (Next)
- Replace Bootstrap 3 navbar with custom CSS
- Replace Bootstrap grid with CSS Grid
- Remove jQuery dependency
- Custom utilities to replace Bootstrap classes

**Phase 4: Icon Migration**
- Replace Glyphicons with Font Awesome 6 classes
- 301 glyphicon references to update
- Add ARIA labels for accessibility

**Phase 5: Accessibility Enhancements**
- Improve semantic HTML
- Add skip-to-content link
- Better heading hierarchy
- ARIA labels on navigation

## Development

### Running the Site

```bash
npm start
# or
node serve-static.js
```

Visit: http://localhost:8080

### Testing Dark Mode

Visit: http://localhost:8080/test-darkmode.html

This page shows:
- Current system theme (light/dark)
- Live CSS variable values
- Color swatches that change with theme

To test theme switching:
1. System Settings → Appearance → Light/Dark
2. Hard refresh browser (Cmd+Shift+R)
3. Or use DevTools: Cmd+Shift+P → "Emulate CSS prefers-color-scheme: dark"

## Project Structure

```
.
├── index.html              # Homepage (static HTML)
├── css/
│   └── site.css           # Modern CSS with dark mode
├── lib/
│   └── bootstrap/         # Bootstrap 3 (TO BE REMOVED in Phase 3)
├── words/                 # Blog posts (nested index.html files)
├── serve-static.js        # Simple dev server (pure Node.js)
├── test-darkmode.html     # Dark mode testing page
├── CHANGELOG.md           # Detailed modernization progress
└── MODERNIZATION.md       # Overview of the modernization approach
```

## Important Technical Details

### Server Quirks

**Query String Handling:** The `serve-static.js` server now properly handles query strings for cache busting. Initially it tried to open files with the query string as part of the filename (e.g., `site.css?v=2` as a literal filename).

**Fixed:** Server now uses `url.parse()` to strip query strings before file lookup.

### Dark Mode

Dark mode works via CSS media queries - no JavaScript required. The browser automatically applies dark mode styles when the system preference is set to dark.

**Key CSS Variables:**
- Light mode: White background (#fefefe), red links (#CC3300)
- Dark mode: Black background (#1a1a1a), orange links (#FF5533)

**Testing:** Bootstrap CSS loads before our custom CSS and sets hardcoded colors. Our CSS variables override Bootstrap's styles. Use hard refresh (Cmd+Shift+R) to bypass browser cache when testing.

### Bootstrap 3 (Temporary)

Bootstrap 3 is still loaded but will be removed in Phase 3. Current strategy:
1. Our modern CSS overrides Bootstrap where needed
2. Still using Bootstrap navbar, grid, and utilities
3. Plan to replace with custom CSS progressively

## Files to Modernize

When adding/updating pages, ensure:
- ✅ Use absolute paths for CSS: `/css/site.css` (not relative)
- ✅ Include preconnect hints for external resources
- ✅ Use HTTPS for all external resources
- ✅ Include SRI integrity hashes on CDN resources
- ✅ No inline styles (use CSS classes/variables)

## Known Issues

1. **Glyphicons don't display** - Font Awesome 6 is loaded but HTML still uses old `glyphicon-*` classes. Will fix in Phase 4.

2. **Bootstrap dependency** - Still loading Bootstrap 3 CSS and JS. Will remove in Phase 3.

3. **jQuery dependency** - Still loaded for Bootstrap navbar. Will remove in Phase 3.

## Workflow Tips

### Making CSS Changes

The CSS uses a comprehensive variable system. To change colors/spacing/fonts:
1. Edit CSS variables at the top of `css/site.css`
2. Changes propagate to entire site
3. Both light and dark mode variables can be customized

### Adding Blog Posts

Blog posts are in `words/YYYY/MM/DD/slug/index.html`. When adding new posts:
1. Copy an existing post as a template
2. Update the content
3. Make sure CSS paths are correct (use absolute paths)
4. Include all meta tags and preconnect hints

### Testing Checklist

Before committing changes:
- [ ] Test in light mode
- [ ] Test in dark mode (toggle system preference)
- [ ] Hard refresh to bypass cache (Cmd+Shift+R)
- [ ] Test on mobile viewport (DevTools)
- [ ] Check browser console for errors
- [ ] Verify all CSS/JS loads (Network tab)

## Resources

- CHANGELOG.md - Detailed phase-by-phase progress
- MODERNIZATION.md - Overview and next steps
- test-darkmode.html - Visual dark mode testing
- serve-static.js - Simple dev server (pure Node.js)

## Notes for Future Work

- The old build system is preserved on `develop` branch if we ever need to reference it
- All modernization commits are co-authored with Claude for tracking
- Use conventional commit messages for each phase
- Update CHANGELOG.md after completing each step
