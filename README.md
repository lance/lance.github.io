# lanceball.com

Lance Ball's personal website - now with modern HTML/CSS!

## Development

Start the local development server:

```bash
npm start
# or
node serve-static.js
```

Then visit http://localhost:8080

## Structure

```
.
├── index.html           # Homepage
├── css/
│   └── site.css        # Modern CSS with dark mode support
├── lib/
│   └── bootstrap/      # Bootstrap 3 (will be removed in Phase 3)
├── words/              # Blog posts
├── serve-static.js     # Simple development server
└── CHANGELOG.md        # Modernization progress
```

## Modernization Progress

This site is being modernized from a Metalsmith/Jade build system to simple static HTML with modern CSS.

✅ **Phase 1: HTTPS & Dependencies** - Complete  
✅ **Phase 2: CSS Modernization** - Complete  
🚧 **Phase 3: Remove Bootstrap** - Pending  
🚧 **Phase 4: Icon Migration** - Pending  
🚧 **Phase 5: Accessibility** - Pending  

See [CHANGELOG.md](CHANGELOG.md) for details.

## Features

- 🎨 Modern CSS with CSS Custom Properties
- 🌓 Automatic dark mode (respects system preference)
- ♿ Improved accessibility
- 📱 Responsive design
- 🚀 No build step required
- 🔒 All external resources use HTTPS with SRI

## License

MIT - See LICENSE.txt
