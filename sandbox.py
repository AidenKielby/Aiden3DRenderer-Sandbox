import tkinter as tk
import pygame
import os
import sys

# Create the main window
window = tk.Tk()

embed = tk.Frame(window, width=640, height=480)
embed.pack()
window.update()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
pygame.display.init()
screen = pygame.display.set_mode((640, 480))
code = ""

window.title("Simple Tkinter Example") # Set window title
def get_text_input():
    global code
    # Get all text from 1st char (1.0) to last (-1c removes newline)
    code = text_widget.get("1.0", "end-1c")


text_widget = tk.Text(window, height=5, width=30)
text_widget.pack()

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

tk.Button(window, text="Get Text", command=get_text_input).pack()
window.mainloop()