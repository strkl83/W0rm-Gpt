# W0rm-GPT Safe Build — design system

Version 1.0 · September 2026

## North star

Make a technical assistant feel trustworthy by showing its boundaries. Every
important state should answer one of three questions at a glance:

1. What is configured?
2. What is happening now?
3. What will this action do?

The system is intentionally technical without adopting an offensive-security
or hacker aesthetic.

## Palette

| Token | Value | Use |
| --- | --- | --- |
| `ink-950` | `#0A0E12` | page background |
| `ink-900` | `#11171D` | primary panels |
| `ink-800` | `#182129` | input and secondary surfaces |
| `ink-700` | `#26323B` | borders and dividers |
| `ink-500` | `#70808B` | muted metadata |
| `ink-200` | `#C9D4D8` | secondary text |
| `paper` | `#EFF5F2` | primary text |
| `mint-500` | `#65E6B0` | active state and primary action |
| `mint-300` | `#A3F4D0` | active text on dark surfaces |
| `amber-400` | `#F2C66D` | configuration and attention |
| `red-400` | `#F28B8B` | errors and blocked actions |

Mint is the product signal. Amber is not an error; it means “needs attention.”
Red is reserved for failure or a blocked action.

## Typography

- Use a neutral sans-serif for headings, controls, and explanatory copy.
- Use a monospace face for prompts, model names, endpoints, status values, and
  code.
- Headings should be short and sentence case.
- Labels are compact and explicit; do not rely on icon-only controls.

## Shape and depth

- Small controls use a 6px radius.
- Panels and inputs use a 10px radius.
- Large feature surfaces use a 16px radius.
- Use one soft panel shadow only for elevated application surfaces. Avoid
  layered glow effects.

## Component states

### Connection status

`Connected` uses mint, `Not configured` uses amber, `Checking` uses a muted
neutral, and `Error` uses red. Each state includes text, never color alone.

### Prompt action

The primary action is mint on ink. Hover increases brightness slightly;
disabled reduces contrast and removes elevation; loading replaces the label
with a short text state such as `Sending`.

### Messages

User messages sit on the slightly raised ink surface. Assistant messages use a
deeper surface with a mint rule or marker. Neither role is communicated by
color alone; include a visible role label.

### Errors

Errors are concise, actionable, and safe to copy. Red styling surrounds the
message but never includes an API key, authorization header, or secret value.

## Motion

Use short opacity and translation transitions for new messages and state
changes. Do not animate continuously. Respect `prefers-reduced-motion`.

## Content rules

- Never claim a response exists when the API was not called.
- Explain configuration as a state, not as a credential.
- Keep safety language calm and specific.
- Do not use emojis, alarmist language, or claims of unrestricted capability.