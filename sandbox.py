import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Simple Tkinter Example") # Set window title
def get_text_input():
    # Get all text from 1st char (1.0) to last (-1c removes newline)
    print(text_widget.get("1.0", "end-1c")) 

text_widget = tk.Text(window, height=5, width=30)
text_widget.pack()

tk.Button(window, text="Get Text", command=get_text_input).pack()
window.mainloop()