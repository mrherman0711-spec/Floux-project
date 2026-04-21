# 🎨 Website Overhaul Prompt for Claude

**Goal**: Transform the current Floux website into a world-class, interactive, elegant experience that makes visitors say "wow" on first load.

**Current State**: Static HTML with basic CSS animations. Functional but lacks polish and visual sophistication.

**Target State**: Premium, motion-rich, sophisticated landing page that converts visitors into demo bookings.

---

## 1. Design System Enhancements

### Typography & Spacing
- Increase letter-spacing subtly across headings (+0.04em for visual breathing)
- Implement variable font weights (300 → 400 → 500 → 600) for hierarchy
- Add kerning adjustments on hero h1 for luxury feel
- Use modular spacing scale: 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px

### Color Palette Expansion
- Keep gold (#9A7B4F) as primary accent
- Add gold-light (#B8956A) for hover states
- Add charcoal-light (#2A2520) for subtle depth
- Add accent-rose (#E8B4A8) for CTA highlights (sparingly)
- Implement CSS custom properties for all colors

### Shadows & Depth
- Add subtle box-shadows to cards: `0 16px 64px rgba(0,0,0,0.24)`
- Create depth layers with layered shadows
- Use shadows on hover for interactive elevation

---

## 2. Animation & Interactivity Framework

### Entrance Animations
- **Hero**: Split h1 into words → stagger each word entering from left (0.1s delay between)
- **Sections**: Reveal elements on scroll with staggered timing (cards pop in sequence)
- **Nav links**: Underline animation on hover (sliding from left)
- **CTAs**: Subtle scale + glow on hover

### Scroll-Driven Animations
- Parallax backgrounds on sections (slower than scroll)
- Counter animation for stats: numbers animate upward when section enters viewport
- Image zoom tied to scroll position (slow, elegant)
- Progress bar at top of page (fills as user scrolls)

### Microinteractions
- Button hover: scale 1.02 + shadow deepens
- Links: underline animation (width 0 → 100% from left)
- Form inputs: gold underline animation on focus
- FAQs: Smooth max-height transition + icon rotation on open/close
- Cards: Subtle shadow shift on hover, slight translateY up

### Page Transitions
- Fade-in on initial load (0.6s ease-out)
- Smooth scroll behavior (already exists, enhance with easing)
- Section dividers: Gradient animates on view (left → right)

---

## 3. Section-by-Section Enhancements

### Hero Section
- **Split-text animation**: Each word of "Recupera los clientes que pierdes mientras trabajas" enters with stagger
- **Background video option**: Replace static image with subtle looping video (salon ambiance, soft, 5-10s loop)
- **Floating elements**: Small decorative gold elements float in background, move on scroll/mouse
- **Gradient text**: Subtitle text has subtle gold gradient on final words
- **Animated CTA buttons**: Buttons have animated border (draws on hover)

### Process Section (Cómo)
- **Card stagger**: Cards slide up from bottom as section enters view, with 0.15s stagger
- **Number counters**: "01" → "02" → "03" count up when visible
- **Overlay animation**: Card overlay brightens/darkens smoothly on hover
- **Image parallax**: Images within cards shift slightly on mouse position (subtle depth)

### Pricing Section
- **Card hover elevation**: Featured card lifts higher, shadow deepens
- **Price counter**: €47 → €97 → €147 animate up when section visible
- **Feature list**: List items fade in with stagger (0.08s between)
- **Interactive comparison**: Hover over one plan → highlight its features, dim others (toggle)

### Why Floux Section
- **Image + text sync**: Text and image enter together, perfectly timed
- **Icon animations**: Small icons (if added) spin on hover
- **Stat numbers**: Increment from 0 to final value (e.g., 0 → +15) with easing function

### FAQs
- **Accordion smooth open**: Max-height transition (0s → 400px) with easing
- **Icon rotation**: Plus icon rotates 45deg to X on open
- **Text reveal**: Answer text fades in as accordion opens
- **Background shift**: Subtle bg color change on open item

### Contact Form
- **Input focus states**: Gold bottom border animates in, label floats up
- **Input validation**: Green checkmark appears on valid input (animated)
- **Submit button**: Animated loader on submit (spinning circle), then success state (checkmark)
- **Form success state**: Entire form fades out, success message animates in from below

### Footer
- **Link hover**: Subtle glow effect + color shift to gold-light
- **Footer scroll**: Slight fade-in as user scrolls toward bottom
- **Social icons** (if added): Hover → rotate + scale

---

## 4. Advanced Features

### Scroll Progress Bar
```
- Thin line at top of page
- Fills left → right as user scrolls
- Color: gradient (gold → rose)
- Height: 2px
- Fixed position, z-index above header
```

### Cursor Effects (Optional)
- Custom cursor (small gold circle)
- Cursor grows on hover over clickable elements
- Cursor changes on different element types (pointer on buttons, text on links)

### Floating Elements
- Small gold accent shapes float in background of sections
- Move subtly with scroll parallax
- Opacity changes based on section

### Loading Animation
- Page load: Fade in (0.6s) with slight blur backdrop
- Hero image: Ken Burns effect (subtle zoom + pan on load)

### Responsive Enhancements
- Mobile animations: Simplified (remove parallax on touch devices)
- Touch-friendly: Larger tap targets, no hover states on mobile
- Swipe gestures: FAQs or testimonials (if added) swipe to navigate

---

## 5. Performance & Best Practices

### CSS Optimization
- Use `will-change` sparingly (only on animated elements)
- GPU acceleration for transforms/opacity
- Debounce scroll listeners
- Use CSS animations over JS where possible

### JavaScript Structure
```
- IntersectionObserver for scroll-triggered animations
- Requestanimationframe for smooth scrolling effects
- Event delegation for form interactions
- No jQuery — vanilla JS only
```

### Accessibility
- All animations have `prefers-reduced-motion` media query
- Aria labels on interactive elements
- Focus states on all inputs/buttons
- Color contrast meets WCAG AA minimum

---

## 6. Specific Animation Timing

| Element | Duration | Easing | Delay |
|---------|----------|--------|-------|
| Hero h1 words | 0.8s | cubic-bezier(0.16,1,0.3,1) | stagger 0.1s |
| Section reveals | 0.9s | cubic-bezier(0.16,1,0.3,1) | on scroll |
| Button hover | 0.3s | ease-out | 0s |
| Card hover shadow | 0.4s | ease | 0s |
| FAQ accordion | 0.45s | ease | 0s |
| Stats counter | 1.2s | ease-out | on scroll |
| Form input focus | 0.25s | ease-out | 0s |

---

## 7. Visual References (Inspiration)

- **Stripe.com**: Smooth section transitions, elegant animations
- **Brex.com**: Premium feel, subtle hover states
- **Linear.app**: Modern, spacious, interactive
- **Figma.com**: Floating elements, smooth scrolling
- **Apple.com**: Minimal motion, maximum impact

---

## 8. Deliverables Expected

1. **Enhanced HTML** with semantic structure
2. **Modular CSS** with animation utilities
3. **Vanilla JavaScript** for interactions (no frameworks)
4. **Mobile-first responsive** design
5. **Performance-optimized** (Lighthouse 90+)
6. **Accessibility-compliant** (WCAG AA)
7. **Cross-browser compatible** (Chrome, Safari, Firefox, Edge)

---

## 9. Testing Checklist

- [ ] Hero animation smooth on all devices
- [ ] Scroll animations trigger at correct viewport points
- [ ] Forms submit and validate with visual feedback
- [ ] All buttons have hover/focus states
- [ ] Mobile animations don't lag
- [ ] Reduced motion preference respected
- [ ] No accessibility violations (axe, WAVE)
- [ ] Lighthouse score 90+ (Performance, A11y, Best Practices)
- [ ] Page load < 3s on 4G
- [ ] All images optimized (WebP with fallback)

---

## 10. Optional Upgrades (Consider After MVP)

- Add customer testimonials carousel (swipeable, auto-play)
- Add live chat widget (Intercom or similar)
- Add video background (hero or sections)
- Add dark mode toggle
- Add language toggle (ES/EN)
- Add newsletter signup (Mailchimp)
- Add Calendly embed for demo booking
- Add trust badges (G2, Trustpilot ratings)
- Add scroll-to-top button (appears after hero)
- Add social proof widgets (# of active salons, €€€ recovered)

---

**Ready to build?** Use this prompt with Claude Code and ask for:
1. "Rebuild the hero section with split-text animation"
2. "Add scroll-triggered animations to all sections"
3. "Create interactive card hover effects"
4. "Build an advanced form with validation feedback"
5. "Optimize for performance and accessibility"

**Let's make it stunning.** 🚀
