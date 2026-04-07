---
name: chrome-devtools-mcp
description: Use when automating Chrome browser tasks — scraping websites, comparing UI designs, taking screenshots, extracting CSS/fonts/colors, clicking elements, filling forms, or performing visual research with the Chrome DevTools MCP.
---

# Chrome DevTools MCP

## Overview

The Chrome DevTools MCP gives Claude direct control over a real Chrome browser: navigate, screenshot, click, scroll, fill forms, and run JavaScript — all without leaving the conversation. Use it for visual research, UI comparisons, scraping, and browser automation.

## Available Tools

| Tool | Purpose |
|------|---------|
| `mcp__chrome-devtools__list_pages` | See open tabs |
| `mcp__chrome-devtools__new_page` | Open URL in new tab |
| `mcp__chrome-devtools__navigate_page` | Go to URL / back / forward / reload |
| `mcp__chrome-devtools__take_screenshot` | Screenshot viewport or full page |
| `mcp__chrome-devtools__evaluate_script` | Run JavaScript on the page |
| `mcp__chrome-devtools__click` | Click element by uid |
| `mcp__chrome-devtools__fill` | Fill a single input |
| `mcp__chrome-devtools__fill_form` | Fill multiple fields at once |
| `mcp__chrome-devtools__scroll` | Scroll by coordinates |
| `mcp__chrome-devtools__wait_for` | Wait for text to appear |
| `mcp__chrome-devtools__take_snapshot` | Accessibility tree snapshot |
| `mcp__chrome-devtools__hover` | Hover over element |
| `mcp__chrome-devtools__press_key` | Send keyboard events |
| `mcp__chrome-devtools__type_text` | Type text into focused element |

## Core Patterns

### 1. Visual Research (e.g. competitor / design analysis)

```
1. new_page(url)
2. take_screenshot()            ← viewport first
3. evaluate_script(() => window.scrollTo(0, Y))
4. take_screenshot()            ← repeat per section
5. evaluate_script(...)         ← extract fonts, colors, CSS vars
```

**Always scroll in steps** (0 → 700 → 1500 → 3000 → bottom). One screenshot per section.

### 2. Extract Design Tokens

```javascript
// Run via evaluate_script
() => {
  const els = document.querySelectorAll('h1, h2, h3, nav, a, p');
  const fonts = new Set(), colors = new Set();
  els.forEach(el => {
    const s = getComputedStyle(el);
    fonts.add(s.fontFamily);
    colors.add(s.color);
    colors.add(s.backgroundColor);
  });
  return { fonts: [...fonts], colors: [...colors] };
}
```

### 3. Read Screenshots

Screenshots save to a temp path. **Always use `Read` tool on the returned file path** to display the image in conversation:

```
take_screenshot(filePath: "/tmp/my-shot.png")
→ Read("/tmp/my-shot.png")   ← makes image visible
```

Or omit `filePath` to get the image inline directly.

### 4. Open Local HTML Files

```
new_page("file:///Users/maxherman/Desktop/Floux%20Project/index.html")
```

URL-encode spaces as `%20`.

### 5. Dismiss Cookie Banners

```javascript
() => {
  for (const el of document.querySelectorAll('*')) {
    if (el.textContent.trim().toUpperCase().includes('ACCEPT') ||
        el.textContent.trim().toUpperCase().includes('ACEPTAR')) {
      el.click(); return 'dismissed';
    }
  }
  return 'not found';
}
```

## Floux-Specific Uses

| Task | How |
|------|-----|
| Compare Floux website to competitor | `new_page(competitor)` → scroll + screenshot → `new_page(index.html)` → scroll + screenshot → diff visually |
| Scrape Treatwell availability | Navigate partner dashboard → evaluate_script to extract slots |
| Scrape Booksy slots | Same pattern as Treatwell |
| Design research | Navigate reference site → extract fonts/colors/layout → apply to index.html |
| Test index.html live | `new_page(file:///...index.html)` → scroll through all sections |

## Tips

- **`evaluate_script` returns JSON** — return values must be serializable
- **`uid` for clicks** — get it from `take_snapshot` accessibility tree
- **Parallel tabs** — use `list_pages` + `select_page` to switch between reference and your site
- **Header transparency** — scroll to 0 first before screenshotting hero sections
- **Remove overlays** via JS if they block content: `document.querySelector('[class*="cookie"]')?.remove()`
- **Scroll parallax** — some hero images won't screenshot correctly mid-page; always screenshot from scroll position 0 for heroes

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Screenshot is blank / wrong section | Call `evaluate_script` to scroll first, then screenshot |
| Can't see screenshot | Use `Read` tool on the saved file path |
| Click not working | Use `take_snapshot` to get correct `uid` |
| JS returns undefined | Ensure function explicitly `return`s a value |
| Cookie banner blocking view | Run dismiss script before screenshotting |
| Local file not loading | URL-encode spaces (`%20`), use `file:///` prefix with full path |
