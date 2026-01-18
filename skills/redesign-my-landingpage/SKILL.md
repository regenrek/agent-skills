---
name: redesign-my-landingpage
description: Build, critique, and iterate high-converting marketing or product landing pages using React + Vite + TypeScript + Tailwind and shadcn/ui components, with all icons sourced from Iconify. Use when the user asks for a landing page, sales page, signup page, CRO improvements, above-the-fold vs below-the-fold structure, hero + CTA copy, section order, or wants production-ready shadcn + Vite code.
---

# Shadcn + Vite landing pages that convert (with Iconify)

## Quick start

1. Identify the single primary conversion action (the one CTA that matters).
2. Draft the page using the anatomy below.
3. Nail above-the-fold first (title, subheadline, visual, proof, CTA).
4. Use below-the-fold to remove doubt (features, proof, FAQ, repeat CTA).
5. Implement in shadcn + Tailwind with a distinctive, intentional aesthetic.

If the user provides an existing page, run the same checklist as an audit and propose specific fixes and A/B tests.

## Default stack and rules

Default stack:
- React + Vite + TypeScript
- Tailwind CSS (prefer v4)
- shadcn/ui components (added via CLI, then customized)
- Iconify icons (no lucide-react)

Rules:
- One primary CTA, one secondary CTA max above the fold.
- One icon family (or at most two) per page.
- Use shadcn components for accessibility and consistency, but do not let them dictate a generic layout.

For project setup commands (Vite + Tailwind + shadcn), see `references/shadcn-vite-setup.md`.

## Core landing page anatomy

Use this default order unless the user has a strong reason to deviate:

1. Navigation (minimal, de-emphasize links that compete with the primary CTA)
2. Hero (value + approach + visual)
3. Social proof (logos, testimonials, numbers)
4. Primary CTA block (repeat CTA if hero is dense)
5. Features (value proof, outcomes, differentiators)
6. CTA repeated 1 to 2 times (after key persuasion moments)
7. Footer (secondary links, legal, contact)

See `references/landing-page-anatomy.md` for the full checklists and annotated examples.

## Above-the-fold checklist

Treat 'above the fold' as the content visible before scrolling on common viewports.

1. Define the value you offer (title)
2. Detail your approach (subheadline)
3. Help the user envision it (visual)
4. Establish credibility (social proof)
5. Simplify the next step (call to action)

Implementation rules:
- Make the primary CTA unmissable.
- Make the visual concrete (product UI, before/after, outcome preview), not decorative.
- Reduce friction with microcopy (no credit card, 60 seconds, cancel anytime).

## Below-the-fold persuasion sequence

1. Show clear value (features)
2. Motivate to action (social proof)
3. Clarify questions (FAQ)
4. Repeat your call to action (CTA)

Add sections only if they remove doubt (pricing, security, comparisons, case studies, integrations).

## Output patterns to produce

Choose the lightest deliverable that satisfies the user's request.

### A) New landing page

Provide:
- Page goal, audience, offer, and primary CTA
- Section-by-section outline mapped to the anatomy
- Hero copy options (3 variations) and CTA microcopy
- Proof plan (what to show and where)
- Implementation: production-grade React code (shadcn + Tailwind + Iconify)

### B) Landing page audit

Provide:
- A short diagnosis: what is the page asking the user to do and is it obvious
- Issues and fixes grouped by: Above-the-fold, Below-the-fold, CTA, Proof, Copy, Design/UX, Performance
- 5 to 10 prioritized recommendations (impact vs effort)
- 3 A/B test ideas with clear hypotheses

## Shadcn component mapping

Prefer these building blocks:
- Navigation: `Button`, `Sheet` (mobile menu), `Separator`
- Hero: `Button`, `Badge`, `Card` (for a framed visual), `Input` (only if email capture is the CTA)
- Social proof: `Card`, `Avatar` (testimonials), `Badge` (press or awards)
- Features: `Card`, `Tabs` (only if comparison is critical)
- FAQ: `Accordion`
- Final CTA: `Card`, `Button`

Add only the components you actually use.

## Icons (Iconify only)

Default icon source: https://icon-sets.iconify.design/

Selection rules:
- Pick one icon set prefix and stay consistent (example: `lucide:*` for a clean outline style).
- Use icons to clarify hierarchy, not to decorate.
- Accessibility: decorative icons should be `aria-hidden="true"`; meaningful icons should have text nearby.

React usage:

```bash
npm i @iconify/react
```

```tsx
import { Icon } from '@iconify/react'

export function IconBullet() {
  return (
    <span className="inline-flex items-center gap-2">
      <Icon icon="lucide:check" aria-hidden="true" className="size-4" />
      <span>Cancel anytime</span>
    </span>
  )
}
```

Notes:
- `@iconify/react` loads icon data on demand by default. Use an offline approach only if the user requires zero network dependence.
- Do not add `lucide-react` unless the user explicitly requests it.

Optional: create an `AppIcon` wrapper for consistent sizing and accessibility. See `references/iconify.md`.

## Design execution (distinctive, non-generic)

Before writing code, decide:
- Purpose: what problem does this page solve and for whom
- Tone: commit to a bold direction (editorial, brutalist, luxury minimal, retro utilitarian, playful, etc.)
- Constraints: performance, accessibility, brand rules
- Differentiation: one memorable detail (layout twist, signature motion moment, unique motif)

Then execute with craft.

Typography
- Choose characterful fonts. Avoid generic defaults.
- Pair one display face (headlines) with a readable body face.

Color and theme
- Use a cohesive palette with 1 to 2 dominant colors and sharp accents.
- Prefer CSS variables (shadcn theme tokens) so the design stays consistent.

Motion
- Use motion as guidance, not decoration: staged reveals, CTA emphasis, proof highlights.
- Prefer a few high-impact moments over many micro animations.

Spatial composition
- Use deliberate hierarchy and whitespace.
- Break the grid only when it improves clarity.

For quick presets, see `references/aesthetic-directions.md`.

## Implementation requirements

- Use semantic HTML and accessible components (labels, focus states, reduced motion support).
- Mobile-first responsive layout.
- Optimize perceived performance: avoid heavy hero media, lazy-load below-the-fold images.
- Keep the primary CTA consistent (label, destination, and promise).

## Included starter asset

If the user asks for a starter page scaffold, use:
- `assets/vite-shadcn-iconify-landing/src/pages/LandingPage.tsx`

This is a sectioned template that matches the anatomy and uses shadcn + Iconify.

## Reference files

- `references/shadcn-vite-setup.md`: install and configure shadcn/ui for Vite (Tailwind, aliases, CLI)
- `references/iconify.md`: Iconify rules + an `AppIcon` wrapper component
- `references/section-templates.md`: copy-paste section templates (Navbar, Hero, Proof, Features, FAQ, CTA, Footer)
- `references/landing-page-anatomy.md`: anatomy, above/below-the-fold checklists, annotated examples
- `references/copy-templates.md`: hero formulas, CTA microcopy, FAQ templates
- `references/aesthetic-directions.md`: bold aesthetic presets to pick from quickly
