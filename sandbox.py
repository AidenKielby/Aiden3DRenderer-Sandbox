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

text_widget = tk.Text(window, height=5)
text_widget.pack(fill="x", pady=(8, 4))

tk.Button(window, text="Get Text", command=lambda: get_text_input()).pack(fill="x", pady=(0, 8))

embed = tk.Frame(window)
embed.bind("<Button-1>", lambda e: focus_pygame())
embed.focus_set() 
embed.pack(fill="both", expand=True)
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

window.title("Simple Tkinter Example") 
def get_text_input():
    global code
    # Get all text from 1st char (1.0) to last (-1c removes newline)
    code = text_widget.get("1.0", "end-1c")
    
    exec(code, exec_env)

def focus_pygame():
    hwnd = pygame.display.get_wm_info()["window"]
    ctypes.windll.user32.SetFocus(hwnd)

def pygame_loop():
    r = exec_env.get("renderer")
    if r is not None:
        r.loopable_run()  # renderer handles keyboard/mouse/events
    window.after(16, pygame_loop)

# Start loops
pygame_loop()

window.after(200, focus_pygame)

window.mainloop()