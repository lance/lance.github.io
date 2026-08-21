# Project: lanceball.com - Static Site Modernization

## Overview

Personal website and blog for Lance Ball. This is the **modernization branch** where we're converting from a Metalsmith/Jade build system to simple static HTML with modern CSS.

---

## 📝 Maintenance Instructions

**IMPORTANT:** This file documents the current state of the project. As work progresses:

✅ **When completing a phase:**
- Move it from "Pending Phases" to "Completed Phases"
- Update the completion date
- Document any key learnings or gotchas

✅ **When discovering new issues:**
- Add them to "Known Issues" section
- Remove them when fixed

✅ **When changing the approach:**
- Update "Development" or "Project Structure" sections
- Document WHY the change was made

✅ **When fixing bugs:**
- Update "Technical Details" with the lesson learned

This ensures future sessions (and future you) understand the current state without re-reading commit history.

---

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

**Phase 3: Remove Bootstrap & jQuery** ✅
- ✅ Replaced Bootstrap navbar with custom CSS
- ✅ Replaced Bootstrap grid with Flexbox
- ✅ Removed jQuery dependency (vanilla JS for mobile menu)
- ✅ Custom utilities replacing Bootstrap classes
- ✅ Deleted all Bootstrap files (~150KB removed!)

**Phase 4: Icon Migration** ✅
- ✅ Font Awesome 6 loaded
- ✅ Converted all glyphicon classes to proper Font Awesome markup
- ✅ Removed CSS shims (no longer needed)
- ✅ Standard, maintainable Font Awesome classes throughout

### 🚧 Pending Phases

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
│   └── site.css           # Modern CSS with dark mode (16KB)
├── images/                # Blog post images
│   ├── circuit-breaker-1.png
│   └── headshot.jpg
├── words/                 # Blog posts (4 total, all modernized)
│   ├── 2016/10/14/data-hiding-in-es6/
│   ├── 2016/11/28/forget-data-encapsulation-embrace-immutability/
│   ├── 2017/01/05/protect-your-node-js-rest-clients-with-circuit-breakers/
│   └── 2017/05/17/riviera-dev-2017/
├── slides/                # Presentation slides (7 decks, 33MB)
│   ├── devnation-live-2018/
│   ├── fullstack-2018/
│   ├── nodeconf-budapest-2017/
│   ├── nodevember2016/
│   ├── red-hat-summit-2018/
│   ├── rhoar-shootout/
│   └── riviera-dev-2018/
├── serve-static.js        # Simple dev server (pure Node.js)
├── test-darkmode.html     # Dark mode testing page
├── modernize-article.py   # Tool to modernize blog posts
├── CHANGELOG.md           # Detailed modernization progress
├── MODERNIZATION.md       # Overview of the modernization approach
└── PHASE3-SUMMARY.md      # Phase 3 completion details
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

None! All major modernization complete. 🎉

**Recently Fixed:**
- ✅ Icons converted to proper Font Awesome 6 classes
- ✅ Bootstrap removed
- ✅ jQuery removed
- ✅ All dependencies modernized
- ✅ All content extracted from master branch

## Workflow Pattern: Iterative Refinement

When you reject a permission request, it often means you want to refine the approach, not abandon it:

**The Pattern:**
1. I ask permission for something (e.g., `git commit` with a message)
2. You reject it
3. You provide feedback: "add this detail..." or "change X to Y"
4. I incorporate the feedback and modify my work
5. I explicitly ask: "OK feedback received. Now do you want to pick up where we left off at [specific command]?"
6. You confirm and we proceed with the refined version

**Important:** A rejection doesn't mean "wrong approach" - it usually means "refine this first."

If you reject without feedback, you're likely tweaking it manually. In that case, I'll wait for you to tell me when to continue.

---

## Workflow Pattern: Clean Up After Tasks

**When completing a task or major milestone:**

1. Check for lingering background processes (especially dev servers)
2. Ask if you want them shut down
3. Clean up temporary files if appropriate

**Common cleanup items:**
- Dev servers on port 8080 (`lsof -ti:8080 | xargs kill -9`)
- Background Node processes
- Temporary build outputs
- Log files

This prevents port conflicts and resource leaks, especially in long sessions where we start/stop servers multiple times.

---

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
