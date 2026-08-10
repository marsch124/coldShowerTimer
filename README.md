# Cold Shower Timer ❄️🚿

A dead-simple timer for cold showers. Set a goal, brace yourself, and let it
count you down — then it flips to a **bonus count-up** so you can push further.

It's a small offline web app (a PWA), so it runs straight from your iPhone's
Home Screen with its own icon — no App Store, no installs, nothing to expire.

## What it does

- **Counts down to your goal** (pick from presets or nudge ±15 s).
- **Chime + a big green screen flash** the instant you hit your goal, with soft
  3-2-1 beeps just before.
- **Keeps going** — after the goal it counts up your bonus time.
- **Keeps the screen awake** during a session so it won't sleep mid-shower.
- **Remembers your last goal** and a friendly summary when you stop.
- **Works fully offline** once added to the Home Screen.

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
