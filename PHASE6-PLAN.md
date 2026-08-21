# Phase 6: Content Management Workflow - Implementation Plan

**Created:** 2026-08-21  
**Status:** Planned (not yet implemented)

## Overview

The current site has excellent static HTML architecture but lacks workflow automation. The solution is a **hybrid approach**: extract boilerplate into templates, create simple generation scripts, and document clear patterns for Claude Code to follow. This keeps the site static while making content management effortless.

---

## 1. Detailed Workflow for Common Tasks

### Workflow 1: Adding a New Blog Post

**Current friction:** 15+ manual steps, error-prone HTML

**New workflow:**

```bash
# Step 1: User runs the new post script
python3 .claude/scripts/new-post.py

# Interactive prompts:
# - Post title: "My New Post"
# - Slug: "my-new-post" (auto-generated from title)
# - Date: 2026-08-21 (defaults to today)

# Step 2: Script generates:
# - Directory: words/2026/08/21/my-new-post/
# - File: words/2026/08/21/my-new-post/index.html (from template)
# - Opens in editor OR Claude reads and assists

# Step 3: User/Claude edits content between markers:
#   <div class="contents">
#     [EDIT CONTENT HERE]
#     <!--more-->  <!-- Everything above this is the excerpt -->
#     [REST OF CONTENT]
#   </div>

# Step 4: Update homepage (automatic or manual)
python3 .claude/scripts/update-homepage.py

# Step 5: Test locally
npm start
# Visit: http://localhost:8080/words/2026/08/21/my-new-post
```

**Claude's role:**
- User says: "Help me write a blog post about X"
- Claude runs `new-post.py`
- Claude drafts content in the generated HTML
- Claude updates homepage
- Claude starts server for preview

**Time saved:** 15 minutes → 2 minutes

---

### Workflow 2: Updating the Homepage

**Current friction:** Manual HTML editing, copy-paste errors

**New workflow:**

```bash
# Option A: Automatic (when adding/removing posts)
python3 .claude/scripts/update-homepage.py

# Option B: Claude-assisted
# User: "Update the homepage"
# Claude: Runs update-homepage.py, shows diff, commits
```

**What the script does:**
- Scans `words/` directory for all blog posts
- Extracts metadata from each post (title, date, excerpt)
- Generates article preview HTML
- Preserves static sections (Projects, Talks)
- Updates only the "Things I've Written" section

---

### Workflow 3: Changing Layout/Styling

**Current friction:** Update navbar in 5 files, footer in 5 files

**New approach: Component Extraction**

Create reference templates:
```
.claude/templates/
├── blog-post.html        # Full blog post template
├── homepage.html         # Homepage structure
├── fragments/
│   ├── head.html        # <head> section
│   ├── navbar.html      # Navigation bar
│   ├── footer.html      # Footer
│   └── scripts.html     # JavaScript includes
```

**Workflow:**

1. **Small changes (CSS variables):** Edit `css/site.css` variables
2. **Structural changes (navbar, footer):**
   ```bash
   # Edit template
   # Run: python3 .claude/scripts/apply-template-changes.py
   # Review diff, commit
   ```

---

## 2. Tools/Scripts Needed

### Script 1: `new-post.py`

**Purpose:** Generate a new blog post from template

**Usage:**
```bash
python3 .claude/scripts/new-post.py [--title "Title"] [--slug slug] [--date YYYY-MM-DD]
```

**What it does:**
1. Prompts for or accepts: title, slug, date
2. Creates directory: `words/YYYY/MM/DD/slug/`
3. Generates `index.html` from template
4. Substitutes: `{{TITLE}}`, `{{DATE}}`, `{{SLUG}}`
5. Prints path to edit

---

### Script 2: `update-homepage.py`

**Purpose:** Regenerate homepage article list from blog posts

**Usage:**
```bash
python3 .claude/scripts/update-homepage.py [--preview]
```

**What it does:**
1. Scans `words/` directory recursively
2. Parses metadata from each `index.html`
3. Generates article preview HTML
4. Updates section between markers in `index.html`

---

### Script 3: `apply-template-changes.py`

**Purpose:** Propagate template changes to all HTML files

**Usage:**
```bash
python3 .claude/scripts/apply-template-changes.py [--component navbar|footer|head|scripts]
```

**What it does:**
1. Reads template from `.claude/templates/fragments/[component].html`
2. Updates all HTML files with component
3. Reports changes made

---

### Script 4: `extract-post-metadata.py`

**Purpose:** Utility to extract metadata from blog posts

**Can be used standalone or by other scripts:**
```bash
python3 .claude/scripts/extract-post-metadata.py words/2017/01/05/*/index.html

# Output (JSON):
{
  "title": "Post Title",
  "date": "Thu Jan 05 2017",
  "url": "/words/2017/01/05/post-title",
  "excerpt": "<p>First paragraph...</p>"
}
```

---

## 3. Templates Structure

Templates are **reference files** for generating/updating HTML:

```
.claude/templates/
├── README.md             # Template documentation
├── blog-post.html        # Full blog post structure
├── homepage.html         # Homepage structure  
└── fragments/
    ├── head.html        # <head> section with meta tags
    ├── navbar.html      # Navigation bar
    ├── footer.html      # Footer
    └── scripts.html     # JavaScript includes
```

**Template Syntax:**
- `{{TITLE}}` - Post title
- `{{DATE}}` - Human-readable date
- `{{DATE_ISO}}` - ISO date (YYYY-MM-DD)
- `{{SLUG}}` - URL slug
- `{{EXCERPT}}` - Post excerpt HTML
- `{{CONTENT}}` - Full post content HTML

**Fragments have marker comments:**
```html
<!-- BEGIN: NAVBAR -->
<nav class="navbar">...</nav>
<!-- END: NAVBAR -->
```

---

## 4. Implementation Steps

### Phase 6.1: Foundation
1. Create `.claude/templates/` directory structure
2. Create `blog-post.html` template (extract from existing post)
3. Create fragment templates
4. Create template README

### Phase 6.2: New Post Script
1. Create `new-post.py` script
2. Implement interactive prompts
3. Implement template substitution
4. Test with Claude

### Phase 6.3: Homepage Update Script
1. Create `extract-post-metadata.py` utility
2. Implement HTML parsing
3. Create `update-homepage.py` script
4. Add markers to current `index.html`
5. Test on existing posts

### Phase 6.4: Template Propagation
1. Create `apply-template-changes.py` script
2. Test on navbar/footer changes
3. Verify all files updated correctly

### Phase 6.5: Documentation
1. Update `CLAUDE.md` with workflows
2. Create `.claude/templates/README.md`
3. Update `.claude/scripts/README.md`
4. Add examples and troubleshooting

### Phase 6.6: Integration Testing
1. Test full blog post workflow
2. Test layout change workflow
3. Test Claude assistance workflow
4. Validate end-to-end

---

## 5. Trade-offs Analysis

### What We're Building

**Advantages:**
- ✅ Simple: Python scripts, no build system
- ✅ Maintainable: Clear code, good documentation
- ✅ AI-Friendly: Claude can run scripts
- ✅ Flexible: Easy to modify
- ✅ Low overhead: Only runs when needed
- ✅ Static output: Site remains pure HTML

**Disadvantages:**
- ⚠️ Manual execution (but Claude can automate)
- ⚠️ Python dependency (already required)
- ⚠️ Not real-time

---

### What We're NOT Building

1. **Full Build System** - No Metalsmith, Hugo, etc.
2. **Templating Engine** - Simple string substitution only
3. **Markdown Support** - Keep HTML control
4. **Database or CMS** - Metadata lives in HTML
5. **Asset Pipeline** - Not needed at this scale

**Reason:** Too much complexity for occasional posts

---

## 6. Success Metrics

**Time Savings:**
- New blog post: 15 min → 2 min (87% reduction)
- Homepage update: 5 min → 10 sec (97% reduction)
- Layout changes: 30 min → 5 min (83% reduction)

**Quality Improvements:**
- Zero manual HTML errors
- Consistent formatting
- Homepage always accurate
- Layout changes propagate reliably

---

## 7. Future Enhancements

Once the basic workflow is proven:

- **Phase 7:** RSS Feed Generation
- **Phase 8:** Tag System
- **Phase 9:** Client-side Search
- **Phase 10:** Image Optimization
- **Phase 11:** Analytics Dashboard

---

## Key Insights from Plan

1. **Templates are reference files**, not a templating engine
2. **Scripts run on-demand**, not automatically
3. **Leverage Claude** for execution and content creation
4. **Keep it simple** - automate repetitive tasks, not creative decisions
5. **Homepage redesigns stay ad-hoc** - don't automate creative work

---

## Next Steps

When ready to implement Phase 6:
1. Review this plan
2. Start with Phase 6.1 (Foundation)
3. Build scripts incrementally
4. Test each script before moving to next
5. Update documentation as you go

---

**This plan keeps the site static and simple while eliminating the friction of managing raw HTML!**
