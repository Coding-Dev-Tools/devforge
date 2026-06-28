# Smell Report — DevForge

**Score: 4/10 — STRONG** (6 tells detected across 10 odors)

## TL;DR

The site has **6 AI-tells**. The structure is competent but reads as the median dark-themed developer tool landing page. The color, type, composition, and proof elements are all domain defaults. A stranger would clock this as generated in under 2 seconds.

## Heuristic Scores

| # | Odor | Detected | Finding |
|---|---|---|---|
| 1 | Tech Gradient | Yes | Indigo-to-purple gradient on every hero heading |
| 2 | Generic Tech Hue | Yes | #6366f1 indigo as primary accent — the default tech color |
| 3 | Feature Tile Grid | Yes | 11 equal product cards, no hierarchy, no priority |
| 4 | Accent Rail | No | Cards use flat borders, no decorative rails |
| 5 | Unearned Blur | No | Nav blur is earned — fixed nav on dark content |
| 6 | Stat Monument | Yes | 5 number clusters with no context, proof, or story |
| 7 | Icon Topper | Faint | Emoji icons serve tool identification but follow template pattern |
| 8 | Bounce Everywhere | No | Subtle 1-2px hover lifts, no elastic or bounce |
| 9 | Default Type | Faint | Inter is documented as intentional but is the domain default |
| 10 | Center Stack | Yes | Hero, stats, CTAs, FAQ all center-aligned by default |

## Domain Default Trap

The visual direction can be guessed from the industry alone: developer tool → dark theme → indigo accent → Inter → centered hero → gradient headline text. The design has not found a project-specific lane.

## What's Working

- **No unearned blur**: Nav glass is functional, not decorative
- **No bounce everywhere**: Motion is restrained to subtle lifts
- **No accent rails**: Cards use clean flat borders
- **Consistent system**: All pages share the same visual language

## Priority Issues

**P0 — Domain Default Trap (Structural)**
Every visual decision can be predicted from "developer CLI tool." Dark #0a0a0b background, indigo accent, Inter typeface, gradient hero text, centered layout. The brief's anti-reference list bans "SaaS-y gradients" but the indigo-purple gradient is the same reflex in dark mode. Fix: recolor or redesign with a non-domain-default palette.

**P1 — Feature Tile Grid (Composition)**
11 equal product cards with no hierarchy. SchemaForge (v1.7.0, 270 tests) gets the same visual weight as tools with no test count. The grid has no editorial judgment — everything is equally important, so nothing is. Fix: relayout to give the strongest tools visual priority.

**P2 — Stat Monument (Evidence)**
"722+ Passing Tests" and "11 Schema Formats" fill space where proof belongs. A number alone proves nothing — there's no before/after, no customer outcome, no demonstration. The stats bar sits above the fold wasting prime real estate. Fix: voice or redesign — replace stat clusters with case language or demonstrated capability.

**P3 — Center Stack (Composition)**
Hero text centered, stats centered, CTAs centered, FAQ centered. Centered is valid when it's a choice, but here it's the default because no composition decision was made. The alternatives page already breaks this with left-aligned comparison tables — the landing page should follow that lead. Fix: relayout.

## Next Modes

- `/design recolor` — break the domain default palette
- `/design relayout` — give product grid hierarchy, kill center-stack defaults
- `/design voice` — replace stat monuments with proof language
- `/design typeset` — commit to a type voice beyond "Inter because it's safe"
