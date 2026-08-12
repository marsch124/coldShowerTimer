# Cold Shower Timer ❄️🚿

A dead-simple timer for cold showers. Set a goal, brace yourself, and let it
count you down — then it flips to a **bonus count-up** so you can push further.

It's a small offline web app (a PWA), so it runs straight from your iPhone's
Home Screen with its own icon — no App Store, no installs, nothing to expire.

## What it does

- **Counts down to your goal** (3 / 6 / 9 min presets, or nudge ±1 min).
- **Three colour-coded phases** — the timer runs blue → yellow → green across
  equal thirds of your goal, so a glance tells you which phase you're in.
- **Chime + a big green screen flash** the instant you hit your goal, with soft
  3-2-1 beeps just before.
- **Keeps going** — after the goal it counts up your bonus time.
- **Multiple profiles** — add a name per person; each keeps their own goal and
  their own history (all stored locally on the device, no account needed).
- **Statistics** — sessions, total time, longest, goal-hit rate, day-streak and
  average, plus three chart views (recent sessions, a calendar heatmap, and
  weekly totals) and a recent-session history.
- **Keeps the screen awake** during a session so it won't sleep mid-shower.
- **Works fully offline** once added to the Home Screen.
- **Settings page** — export a backup of all your data (and restore it on any
  device), a collapsible "How this works" guide, and a dated version log of what
  changed and why.

## Version history

The full, dated log lives inside the app (**Settings → Version log**). Recent
highlights:

- **v1.10** — Fresh updates arrive faster: the app now fetches itself with the
  browser cache bypassed, so a newly published version shows up right after you
  close and reopen it.
- **v1.9** — Fixed the pale strip that could show along the very bottom edge on
  iPhone (the home-indicator area) by painting a solid background colour across
  the whole screen behind everything.
- **v1.8** — Punchier green finish (brighter, more vivid "you made it" wash) and
  a slightly smaller bonus "+" count-up so it sits neatly inside the ring.
- **v1.7** — Version number now shown under the tagline on the home screen.
- **v1.6** — Friendlier, rounded coral delete button in Stats → Adjust.
- **v1.5** — 30-second test timer, an "Adjust" tool to add/delete past sessions,
  a redesigned Settings gear icon, and an expanded "How this works" guide.
- **v1.4** — Green "you made it" background that stays green through the bonus.
- **v1.3** — Settings page: data backup/restore, guide, and version log.
- **v1.2** — Multiple profiles and a full statistics screen.
- **v1.0** — Installable, fully-offline PWA with Home Screen icons.

## Use it on your iPhone

1. Open the app's web address in **Safari**.
2. Tap the **Share** button → **Add to Home Screen**.
3. Launch it from the new **Cold Shower** icon — it opens full-screen like a real app.

> Tip: the chime needs sound on, so make sure your phone isn't on silent (or
> keep an eye out for the green flash, which always fires).

## Project layout

```
ColdShowerTimer/
├─ index.html              # the whole app (UI + logic, self-contained)
├─ manifest.webmanifest    # PWA metadata (name, icons, colours)
├─ service-worker.js       # offline caching
├─ icons/                  # app icons (generated)
├─ tools/
│  └─ make_icons.py        # regenerates the icons (no libraries needed)
└─ README.md
```

## Developing / previewing locally

The app needs to be served over `http://` (service workers don't run from
`file://`). Any static server works, e.g.:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

To regenerate the icons after tweaking the design:

```bash
python3 tools/make_icons.py
```

## License

[MIT](LICENSE) — do whatever you like with it.
