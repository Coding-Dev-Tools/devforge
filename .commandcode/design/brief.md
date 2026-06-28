# DevForge Design Brief

## Register
**Brand** — marketing landing page, pricing, blog, docs, about. The interface is the experience. Emotional reaction at arrival is the deliverable.

## Users & Context
- Primary: Software engineers evaluating CLI tools for their workflow
- They arrive with a specific problem (API contracts, config drift, dead code, schema conversion) and need to know in 5 seconds whether this solves it
- Secondary: Engineering managers comparing tool ecosystems, pricing, and team fit
- Pressure: they're losing time to problems that should have been caught in CI — they need evidence this works, not promises

## Product Purpose
11 open-source CLI tools that catch engineering problems before production — API contract violations, config drift, infrastructure cost surprises, dead code, schema conversion friction. Install with pip, no account, no dashboard, no lock-in.

## Voice
- Direct and technical. No marketing padding. No exclamation points.
- The copy names real problems developers face at 2 AM when a deploy goes wrong
- Confident without bragging — the tools speak through test counts, CI exit codes, and concrete workflows
- Sentence case everywhere. One verb per button.

## Anti-References
- No SaaS-y gradients (blue-purple-to-cyan is banned)
- No dashboard screenshots, no fake UI chrome, no platform metaphors
- No "unleash your potential" or "supercharge your workflow" language
- No centered hero with floating 3D isometric illustration
- No testimonials with stock headshots
- No "trusted by thousands" when the tools are beta

## Design Principles
1. **Evidence over decoration** — 722+ tests, exit code 1 on failure, real CLI output. Every visual element must earn its space
2. **Dark by default** — the site lives in a terminal-like space (#0a0a0b) because the tools are CLI-first
3. **One thing per section** — each tool card, each stat, each blog post stands alone. No nested cards
4. **Speed reads as quality** — pip install in seconds, CI gates in minutes. The site should feel as fast as the tools
5. **The proof is the output** — show real CLI output, real diffs, real exit codes. Never replace with mockups

## Visual Foundation

### Typography
- **Family:** Inter (weights 400, 500, 600, 700, 800), fallback to system sans-serif
- **Scale:**
  - Hero heading: 3.2rem / 800 / -0.04em letter-spacing
  - Section heading: 2rem / 700 / -0.03em
  - Subsection heading: 1.1rem / 600
  - Body: 0.95rem / 400
  - Small/caption: 0.8rem / 400
- **Measure:** 600px max for body paragraphs, 1100px max-width site container

### Color System
- **Background:** #0a0a0b (near-black)
- **Surface:** #121213 (cards), #1a1a1c (secondary buttons)
- **Border:** #1e1e20 (default), #2a2a2d (hover)
- **Text:** #fff (headings), #e1e1e3 (body), #888 / #999 (muted), #555-666 (captions)
- **Accent:** #6366f1 (indigo primary), #a78bfa (purple secondary, gradient pair)
- **Success:** #34d399 (checkmarks, ready status)
- **Warning:** #f59e0b (status)
- **Tag colors:** semantic only — indigo for versions, green for free/pro, dim gray for category tags

### Layout
- Max-width: 1100px center-aligned
- Nav: fixed, glass (rgba(10,10,11,0.85) + backdrop-blur 12px)
- Product grid: auto-fill, minmax(340px, 1fr), 20px gap
- Pricing grid: auto-fill, minmax(280px, 1fr), 20px gap
- Section padding: 80px 24px
- Cards: 14px border-radius, 28px internal padding, 1px border
- Stats bar: horizontal flex, 48px gap, centered

### Component Rules
- **Buttons:** 10px border-radius, 600 weight, no box-shadow. Primary = accent fill + white text. Secondary = dark surface + border
- **Cards:** flat surface #121213, 1px border, hover raises border to #2a2a2d with translateY(-2px)
- **Tags/pills:** 6px radius, 3px-10px padding, 0.7rem, 500 weight, background tinted 12% of text color
- **Inputs:** dark surface #121213, 1px border #2a2a2d, accent on focus
- **Nav links:** 0.85rem, #888 default, #fff on hover, 28px gap

### Motion
- Nav: backdrop-blur with border, no entrance animation
- Cards: 0.15s transition on hover (border-color + 2px lift)
- Buttons: 0.15s transition on hover (background + 1px lift)
- No page-load animations, no scroll reveals, no stagger effects
- `prefers-reduced-motion`: remove translateY transforms, keep color transitions

## Accessibility
- All text meets 4.5:1 contrast against background
- Focus visible on all interactive elements
- Nav is semantic, links are real anchors
- Form inputs have visible labels (email waitlist)
- Keyboard navigable

## Pages
- `index.html` — landing: hero, stats, product grid, pricing summary, blog preview, FAQ, CTA
- `pricing.html` — full pricing table with feature comparison
- `blog.html` — blog index with full post listing, RSS link
- `about.html` — mission, story/timeline, AI agent team, tutorial links
- `start-here.html` — tool finder/decision guide
- `docs.html` — documentation overview
- `quickstart.html` — getting started guide
- `alternatives.html` — competitor comparison
- `releases.html` — changelog
