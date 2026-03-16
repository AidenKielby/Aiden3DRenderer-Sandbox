# Aiden3DRenderer Sandbox

A desktop sandbox for live-driving your `aiden3drenderer` scene code inside an embedded `pygame` viewport, wrapped in a polished `tkinter` UI.

This project is built for rapid iteration:
- Edit scene code in the top editor pane
- Click **Run Script**
- See results immediately in the embedded 3D viewport

---

## Overview

`Aiden3DRenderer Sandbox` is a single-file local tool (`sandbox.py`) that combines:
- `tkinter` for the host window and script editor
- `pygame` for the real-time render surface
- `aiden3drenderer` for 3D rendering

The app includes:
- Resizable split layout (code editor + viewport)
- Keyboard forwarding from Tk to pygame
- Click-to-focus behavior for viewport input
- Hot script execution via **Run Script**

---

## Project Structure

```text
Aiden3DRenderer sandbox/
├─ sandbox.py
└─ README.md
```

---

## Requirements

- Python 3.10+
- `pygame`
- `aiden3drenderer` (installed and importable)
- Windows (current embedding/focus behavior is tuned for Win32 via `ctypes`)

Install dependencies:

```bash
pip install pygame
```

Install your renderer package (example):

```bash
pip install aiden3drenderer
```

If your package is local, install in editable mode from the package root:

```bash
pip install -e .
```

---

## Quick Start

Run the app:

```bash
python sandbox.py
```

Inside the app:
1. Edit code in the top text pane.
2. Click **Run Script**.
3. Click inside the viewport to focus pygame controls.

---

## Default Script

On startup, the editor preloads this base snippet:

```python
embed_w = embed.winfo_width()
embed_h = embed.winfo_height()
renderer = Renderer3D(width=embed_w, height=embed_h, title="My 3D Renderer")
renderer.current_shape = "waves"
renderer.render_type = renderer_type.MESH
```

You can replace or extend it, then rerun with **Run Script**.

---

## Input and Focus Behavior

### Keyboard forwarding
The sandbox maps Tk key events into pygame events for common controls:
- `W`, `A`, `S`, `D`
- `Space`, `Shift`, `Ctrl`
- Arrow keys
- `Escape`

`Escape` also toggles pause menu state in the active renderer (if present).

### Editor lock while viewport focused
When viewport focus is activated, text editing is temporarily disabled to avoid accidental typing while controlling the camera/scene.
- Click inside editor text to re-enable editing.
- Click inside viewport to return focus to pygame.

---

## Layout

The UI uses a vertical `PanedWindow`:
- Top pane: script editor + run button
- Bottom pane: embedded pygame viewport

You can drag the sash to resize how much space each pane receives.

---

## Troubleshooting

### Window dragging feels glitchy
If the main window snaps back while moving, auto-forcing focus to pygame can interfere with top-level window interactions.

Try:
- Removing delayed auto-focus calls such as `window.after(200, focus_pygame)`
- Avoiding forced focus after each script run
- Keeping pygame focus manual (click viewport)

### "Run Script" appears to do nothing
Common causes:
- Code did not change between runs
- New script raised an exception (check console output)
- Existing renderer instance wasn’t reset before re-exec

Current sandbox behavior resets `exec_env["renderer"]` before executing your script.

### FOV changes do not apply
If changing `renderer.fov` has no visual effect, the renderer package may cache projection values once and never rebuild them. Verify `aiden3drenderer` recomputes projection math whenever FOV changes.

---

## Development Notes

- The app embeds pygame by setting `SDL_WINDOWID` from a Tk frame.
- The render loop runs through `window.after(16, ...)` for ~60 FPS scheduling.
- Script execution occurs via `exec(code, exec_env)`.

Because execution is dynamic, only run trusted code in the editor pane.

---

## Future Improvements

- Add in-app error panel (instead of console-only errors)
- Add script presets and save/load actions
- Add explicit renderer lifecycle hooks for safe reruns
- Add hotkeys for run/focus toggle
- Add optional light theme

---

## License

Add your preferred license here (for example: MIT).
