---
paths: ["*.html"]
---
# Design System

## Colors
--dark: #1A1714 (primary background — warm dark charcoal, NOT pure black)
--cream: #F2EDE6 (primary text/light)
--gold: #9A7B4F (accent)
--gold-h: #7D6340 (gold hover)
--footer-bg: #0E0C0A
--light: #DED8D0
--body: #6B6560

## Typography
- Headings: Cormorant Garamond (Google Fonts) — weight 300/400
- Body: Inter — weight 300/400/500
- Eyebrows: Cormorant SC, 0.32em letter-spacing, uppercase, gold
- h2: Cormorant SC, uppercase, 0.14em letter-spacing
- Body text opacity: minimum 0.75 (never 0.55 — illegible)

## Buttons
- Zero border-radius
- Outlined, transparent fill
- ALL CAPS, 0.2em letter-spacing, 0.6875rem
- Primary: cream border/text, hover fills cream
- Outline: gold border/text, hover fills gold

## Nav
- Fixed, dark charcoal bg
- ALL CAPS links, 0.18em letter-spacing, 0.625rem
- Height: 76px

## Hero
- Full-bleed 100vh image with gradient overlay
- Copy positioned bottom-left
- Gradient: rgba(26,23,20,0.85) bottom → rgba(26,23,20,0.15) top

## Effects
- Scroll reveal: .reveal class + IntersectionObserver fade-up
- Images: .img-zoom (hover zoom) + .img-gold-tint (gold overlay)
