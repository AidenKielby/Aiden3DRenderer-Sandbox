import tkinter as tk
import pygame
import os
from aiden3drenderer import *
import ctypes

# Create the main window
window = tk.Tk()
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
window.geometry(f"{screen_w}x{screen_h}+0+0")
window.geometry("1200x800+100+100")
window.minsize(600, 400)
window.title("Aiden 3D Renderer Sandbox")

# Visual styling only (no behavior changes)
APP_BG = "#101418"
PANEL_BG = "#171d24"
TEXT_BG = "#0f141a"
TEXT_FG = "#dce8f5"
ACCENT = "#4fa3ff"

window.configure(bg=APP_BG)

text_widget = tk.Text(
    window,
    height=5,
    bg=TEXT_BG,
    fg=TEXT_FG,
    insertbackground=TEXT_FG,
    selectbackground=ACCENT,
    selectforeground="#ffffff",
    relief="flat",
    highlightthickness=1,
    highlightbackground="#253242",
    highlightcolor=ACCENT,
    padx=10,
    pady=8,
    font=("Segoe UI", 11),
)
text_widget.pack(fill="x", padx=12, pady=(12, 6))

tk.Button(
    window,
    text="Run Script",
    command=lambda: get_text_input(),
    bg=ACCENT,
    fg="#ffffff",
    activebackground="#3a8fe8",
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    padx=12,
    pady=8,
    font=("Segoe UI Semibold", 10),
    cursor="hand2",
).pack(fill="x", padx=12, pady=(0, 10))

embed = tk.Frame(window, bg=PANEL_BG, bd=1, relief="solid", highlightthickness=1, highlightbackground="#253242")
embed.bind("<Button-1>", lambda e: focus_pygame())
embed.focus_set() 
embed.pack(fill="both", expand=True, padx=12, pady=(0, 12))
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
exec_env = {"renderer": None, "embed": embed, "Renderer3D": Renderer3D, "renderer_type": renderer_type}

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
    # Get all text from 1st char (1.0) to last (-1c removes newline)
    code = text_widget.get("1.0", "end-1c")
    
    exec(code, exec_env)

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

window.after(200, focus_pygame)

window.mainloop()