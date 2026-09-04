# W0rm-GPT design system instructions

Use this document whenever a future UI artifact is created for this project.
The product is a safe, transparent command-line assistant, not a hacking tool.
The interface should make network behavior, configuration, and safety boundaries
easy to understand.

## Product identity

W0rm-GPT Safe Build is a focused terminal companion for people who want to ask
an OpenAI-compatible model questions without hidden execution, opaque binaries,
or silent updates. It should feel like a trustworthy instrument: precise,
quietly technical, and direct about what it can and cannot do.

## Visual language

- Use a dark graphite foundation with mint-green signal accents and amber
  configuration states.
- Keep surfaces layered and calm; avoid neon cyberpunk, skulls, terminal
  clichés, or visual cues that glamorize unauthorized access.
- Prefer compact technical labels, short explanations, and visible system
  status.
- Do not use emojis anywhere in the UI.
- Use motion only to clarify state changes: connection checks, message arrival,
  and validation feedback.

## Design tokens

```css
--color-ink-950: #0a0e12;
--color-ink-900: #11171d;
--color-ink-800: #182129;
--color-ink-700: #26323b;
--color-ink-500: #70808b;
--color-ink-200: #c9d4d8;
--color-paper: #eff5f2;
--color-mint-500: #65e6b0;
--color-mint-300: #a3f4d0;
--color-amber-400: #f2c66d;
--color-red-400: #f28b8b;
--radius-sm: 6px;
--radius-md: 10px;
--radius-lg: 16px;
--shadow-panel: 0 18px 50px rgba(0, 0, 0, 0.24);
--font-sans: Inter, ui-sans-serif, system-ui, sans-serif;
--font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
```

## Required component behavior

- **App shell:** Always show product name, current provider, model, and
  connection state.
- **Prompt composer:** The primary action must be obvious, keyboard
  accessible, and disabled while a request is in flight.
- **Message stream:** Distinguish user and assistant messages by alignment and
  surface treatment, not color alone.
- **Status badge:** Use `connected`, `not configured`, `checking`, and `error`
  states with text labels and accessible contrast.
- **Safety notice:** Explain that the app does not execute downloaded code or
  silently update itself.
- **Error state:** Show the provider's actionable message without exposing
  secrets, headers, or raw credentials.
- **Empty state:** Explain how to start with one example prompt; never imply
  that a response was generated when the API is unavailable.

## Accessibility and content

- Meet WCAG AA contrast for text and controls.
- Preserve visible focus rings.
- Use semantic headings, labels, and live regions for new responses.
- Keep copy factual and compact. Say “API key configured” rather than
  displaying or previewing a key.
- Never display secret values, even partially.