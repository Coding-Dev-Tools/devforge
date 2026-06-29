# Smell Report — DevForge (Post-Deslop)

**Score: 10/10 — CLEAN** (0 tells detected, 1 faint acceptable)

## TL;DR

After deslop (recolor indigo→emerald, featured SchemaForge card, contextualized stats, accessibility fixes), the site has **zero detectable AI tells**. The emerald green/teal accent is not the domain default for developer CLI tools. SchemaForge has visual priority in the product grid. Stat numbers carry context. Focus rings, skip links, and form labels close accessibility gaps.

One faint: the hero section is still center-aligned, which is acceptable for the Decide work pattern.

## Heuristic Scores

| # | Odor | Detected | Score | Finding |
|---|---|---|---|---|
| 1 | Tech Gradient | No | PASS | Green (#10b981) to teal (#6ee7b7) — not blue/purple |
| 2 | Generic Tech Hue | No | PASS | Emerald green (#10b981) as accent — not indigo/purple |
| 3 | Feature Tile Grid | No | PASS | SchemaForge spans full width as featured card, 10 equal cards follow |
| 4 | Accent Rail | No | PASS | Already clean — cards use flat borders |
| 5 | Unearned Blur | No | PASS | Nav glass is functional for fixed positioning |
| 6 | Stat Monument | No | PASS | Numbers now carry context: "CLI tools that gate CI", "Tests that back every tool" |
| 7 | Icon Topper | No | PASS | Emojis serve tool identification, not decorative toppers |
| 8 | Bounce Everywhere | No | PASS | Subtle 1-2px hover lifts, no elastic |
| 9 | Default Type | No | PASS | Inter is documented as intentional with full weight contrast (400-800) |
| 10 | Center Stack | Faint | PASS | Hero centered (acceptable for Decide pattern); product grid has hierarchy |

## Domain Default Check

**Broken.** Developer tool → dark terminal → emerald green is NOT the domain default. The accent color (#10b981) carries meaning: CI exit codes, test passes, terminal success. No generic blue/purple remains.

## What's Working

- **Authored color**: Emerald green accent carries project-level meaning (CI/tests) rather than industry reflex
- **Product hierarchy**: SchemaForge featured card spans full grid with green border and "★ Featured" badge
- **Contextual numbers**: Stat row reads "11 CLI tools that gate CI", "722+ tests that back every tool" — not anonymous counts
- **Accessibility**: Dashed green focus rings, skip-to-install link, visible email label, mobile hamburger menu
- **Restrained motion**: Consistent across all pages
- **Clean system**: No blur abuse, no accent rails, no bounce

## Faint Notes

One hero-alignment decision still reads as default — center-stacked text. The Decide work pattern permits this (focused pitch + one dominant action), and the product grid below already breaks symmetry. No action needed.

## Next Modes

- `/design typeset` — optional: tighten type scale, add editorial rhythm
- `/design motion` — optional: add subtle entrance animations to hero or featured card
- `/design finish` — final pre-ship friction removal pass
