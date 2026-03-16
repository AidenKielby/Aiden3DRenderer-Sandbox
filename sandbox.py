import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
from aiden3drenderer import *
import ctypes

# Create the main window
window = tk.Tk()
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
window.geometry("1200x800+100+100")
window.minsize(600, 400)
window.title("Aiden 3D Renderer Sandbox")

# Visual styling only (no behavior changes)
APP_BG = "#101418"
PANEL_BG = "#171d24"
TEXT_BG = "#0f141a"
TEXT_FG = "#dce8f5"
ACCENT = "#4fa3ff"
ACCENT_HOVER = "#68b3ff"
ACCENT_ACTIVE = "#3a8fe8"
BORDER = "#253242"
SUBTEXT = "#95a9bf"

window.configure(bg=APP_BG)
window.option_add("*Font", "{Segoe UI} 10")

split = tk.PanedWindow(
    window,
    orient="vertical",
    sashwidth=8,
    bd=0,
    bg=APP_BG,
    relief="flat",
    opaqueresize=True,
)
split.pack(fill="both", expand=True, padx=12, pady=12)

top_panel = tk.Frame(split, bg=APP_BG)
toolbar = tk.Frame(top_panel, bg=APP_BG)
toolbar.pack(fill="x", pady=(0, 6))

tk.Label(
    toolbar,
    text="Script Editor",
    fg=SUBTEXT,
    bg=APP_BG,
    font=("Segoe UI Semibold", 10),
).pack(side="left")

run_button = tk.Button(
    toolbar,
    text="Run Script",
    command=lambda: get_text_input(),
    bg=ACCENT,
    fg="#ffffff",
    activebackground=ACCENT_ACTIVE,
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    padx=14,
    pady=7,
    font=("Segoe UI Semibold", 10),
    cursor="hand2",
)
run_button.pack(side="right")

run_button.bind("<Enter>", lambda e: run_button.config(bg=ACCENT_HOVER))
run_button.bind("<Leave>", lambda e: run_button.config(bg=ACCENT))

# Save / Load buttons
def _make_tool_button(parent, text, cmd):
    b = tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=APP_BG,
        fg=TEXT_FG,
        activebackground=BORDER,
        relief="flat",
        bd=0,
        padx=8,
        pady=6,
        cursor="hand2",
        font=("Segoe UI", 9),
    )
    b.bind("<Enter>", lambda e: b.config(bg="#11151a"))
    b.bind("<Leave>", lambda e: b.config(bg=APP_BG))
    return b

def save_script():
    prev = text_widget.cget("state")
    try:
        if prev == "disabled":
            text_widget.config(state="normal")
        data = text_widget.get("1.0", "end-1c")
        path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            title="Save script as...",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        messagebox.showinfo("Saved", f"Script saved to:\n{path}")
    finally:
        text_widget.config(state=prev)

def load_script():
    path = filedialog.askopenfilename(
        defaultextension=".py",
        filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        title="Open script...",
    )
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")
        return
    text_widget.config(state="normal")
    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", data)
    messagebox.showinfo("Loaded", f"Script loaded from:\n{path}")

load_btn = _make_tool_button(toolbar, "Load", load_script)
load_btn.pack(side="right", padx=(6, 0))
save_btn = _make_tool_button(toolbar, "Save", save_script)
save_btn.pack(side="right", padx=(6, 0))

text_widget = tk.Text(
    top_panel,
    height=5,
    bg=TEXT_BG,
    fg=TEXT_FG,
    insertbackground=TEXT_FG,
    selectbackground=ACCENT,
    selectforeground="#ffffff",
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
    padx=10,
    pady=8,
    font=("Segoe UI", 11),
    undo=True,
    autoseparators=True,
    maxundo=-1,
)
text_widget.pack(fill="both", expand=True)

# Informational note about renderer limitations
note_text = (
    "Note: Some visuals may appear warped; changing FOV may not take effect "
)
tk.Label(top_panel, text=note_text, fg=SUBTEXT, bg=APP_BG, wraplength=900, justify="left").pack(fill="x", pady=(8, 4))

embed = tk.Frame(
    split,
    bg=PANEL_BG,
    bd=1,
    relief="solid",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
)
embed.bind("<ButtonRelease-1>", lambda e: focus_pygame())
embed.focus_set()

split.add(top_panel, minsize=120)
split.add(embed, minsize=200)
window.after(50, lambda: split.sash_place(0, 0, 220))

window.update_idletasks()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
pygame.display.init()
screen = pygame.display.set_mode((max(1, embed.winfo_width()), max(1, embed.winfo_height())))
code = """

"""

base_code = """
embed_w = embed.winfo_width()
embed_h = embed.winfo_height()
renderer = Renderer3D(width=embed_w, height=embed_h, title="My 3D Renderer")
renderer.current_shape = "waves"
renderer.render_type = renderer_type.MESH
"""


text_widget.insert("1.0", base_code)
exec_env = {"renderer": None, "embed": embed, "Renderer3D": Renderer3D, "renderer_type": renderer_type, "obj_loader": obj_loader, 
            "register_shape": register_shape, "Camera": Camera, "physics": physics, "dae_loader": dae_loader, "VideoRenderer3D": VideoRenderer3D, 
            "VideoRendererObject": VideoRendererObject, "Button": Button}

TK_TO_PG = {
    "w": pygame.K_w, "a": pygame.K_a, "s": pygame.K_s, "d": pygame.K_d,
    "space": pygame.K_SPACE, "Shift_L": pygame.K_LSHIFT, "Shift_R": pygame.K_RSHIFT,
    "Control_L": pygame.K_LCTRL, "Control_R": pygame.K_RCTRL,
    "Up": pygame.K_UP, "Down": pygame.K_DOWN, "Left": pygame.K_LEFT, "Right": pygame.K_RIGHT,
    "Escape": pygame.K_ESCAPE,
}

pressed = set()

def on_key_press(e):
    k = TK_TO_PG.get(e.keysym)
    if k is None:
        return
    
    # If the key is not currently held down
    if k not in pressed:
        pressed.add(k)  # Mark it as held down
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=k, mod=pygame.key.get_mods()))
        
        # Add the custom toggle logic here for exactly one press
        if k == pygame.K_ESCAPE:
            r = exec_env.get("renderer")
            if r is not None:
                r.show_pause_menu = not r.show_pause_menu
                r.show_settings_menu = False

def on_key_release(e):
    k = TK_TO_PG.get(e.keysym)
    if k is None:
        return
    if k in pressed:
        pressed.remove(k)
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=k, mod=pygame.key.get_mods()))

window.bind_all("<KeyPress>", on_key_press)
window.bind_all("<KeyRelease>", on_key_release)

def get_text_input():
    global code
    code = text_widget.get("1.0", "end-1c")

    # Stop/reset previous renderer so rerun is visible
    old_renderer = exec_env.get("renderer")
    if old_renderer is not None:
        # If your renderer has cleanup/shutdown methods, call them here.
        for method_name in ("cleanup", "shutdown", "close", "quit"):
            method = getattr(old_renderer, method_name, None)
            if callable(method):
                try:
                    method()
                except Exception:
                    pass
                break

    exec_env["renderer"] = None

    try:
        exec(code, exec_env)
        #focus_pygame()  # put focus back to pygame after rerun
    except Exception as e:
        print("Script error:", e)

def enable_text_editing(event=None):
    text_widget.config(state="normal")
    text_widget.focus_set()

def disable_text_editing():
    text_widget.config(state="disabled")
    embed.focus_set()

def focus_pygame():
    disable_text_editing() 
    hwnd = pygame.display.get_wm_info()["window"]
    ctypes.windll.user32.SetFocus(hwnd)

def pygame_loop():
    r = exec_env.get("renderer")
    if r is not None:
        r.loopable_run()  # renderer handles keyboard/mouse/events
    window.after(16, pygame_loop)

text_widget.bind("<Button-1>", enable_text_editing)

# Start loops
pygame_loop()

#window.after(200, focus_pygame)

window.mainloop()