import tkinter as tk
import pygame
import os
from aiden3drenderer import *

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
embed.bind("<Button-1>", lambda e: embed.focus_set())
embed.focus_set() 
embed.pack(fill="both", expand=True)
window.update_idletasks()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
pygame.display.init()
screen = pygame.display.set_mode((max(1, embed.winfo_width()), max(1, embed.winfo_height())))
code = ""

window.title("Simple Tkinter Example") 
def get_text_input():
    global code
    # Get all text from 1st char (1.0) to last (-1c removes newline)
    code = text_widget.get("1.0", "end-1c")

def pygame_loop():
    """Handles Pygame events and updates."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.destroy()
            return
    exec(code)
    pygame.display.flip()
    window.after(16, pygame_loop)  # ~60 FPS

# Start loops
pygame_loop()

window.mainloop()