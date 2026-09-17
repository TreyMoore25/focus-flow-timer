# Trey's Focus Flow

A single-file productivity dashboard built around the Pomodoro technique. No dependencies, no build step — open the HTML file in any browser and go.

## Features

**Timer**
- Configurable session length via quick-pick buttons (5, 15, 25, 45, 60 min) or a custom H/M/S input
- Optional task name field — set what you're working on before starting; carries through to the focus log, note prompt, and text report
- Circular progress ring with animated gradient stroke
- Start, pause, and reset controls
- Automatic break prompt after each focus block (5 min short / 15 min long)

**Visualization**
- Animated Strawberry Açaí cup that fills as sessions are completed
- Animated starfield background — stars rush toward the viewer as you work
- Session completion dots track your daily Pomodoro count

**To-Do List**
- Workflow: **Start** a task to move it into In Progress (also loads its name into the timer's task field); **Complete** opens a modal to record how long it took, moving it to Done
- Add and delete tasks; schedule for Today/Tomorrow/Later
- Persisted in `localStorage` — survives page reloads

**Focus Log**
- Each completed session prompts for an optional note
- Log groups entries by hour, showing 12-hour timestamps (e.g. `2:15 PM – 2:40 PM`)
- Delete individual entries
- Copy the full day's log as a formatted text report, or export it as a `.txt` or `.csv` file

**Integrations**
- **Alarm sound themes** — choose from Beeps, Chime, Bell, or Pulse; clicking previews the sound immediately

**Browser notifications**
- Break reminders fire a native browser notification when a session ends (requires permission)

## Usage

1. Download or clone the repo
2. Open `Acai timer.html` in any modern browser

No server, no npm install, no config files.

## Open PRs

| # | Feature | Branch |
|---|---------|--------|
| [#1](https://github.com/TreyMoore25/focus-flow-timer/pull/1) | Break reminders via browser notifications | `feature/break-reminders` |
| [#2](https://github.com/TreyMoore25/focus-flow-timer/pull/2) | Weekly summary modal | `feature/weekly-summary` |
| [#3](https://github.com/TreyMoore25/focus-flow-timer/pull/3) | Per-entry Slack send button | `feature/slack-manual-send` |
| [#4](https://github.com/TreyMoore25/focus-flow-timer/pull/4) | Selectable alarm sound themes | `feature/sound-themes` |

## Tech

- Vanilla HTML / CSS / JavaScript — single file, zero dependencies
- Web Audio API for synthesized alarm sounds (no audio files)
- Canvas API for the animated starfield
- SVG for the progress ring and cup visualization
- `localStorage` for all persistence (log, todos, webhook URL, sound preference)
