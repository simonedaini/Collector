import keyboard
import tkinter as tk

window = tk.Tk()
label = tk.Label(text="Time")
label.pack()
time = tk.Entry()
time.pack()
button = tk.Button(text="Insert")
button.pack()

window.mainloop()
# modicia
# while True:
#     pressed = keyboard.read_key()
#     if pressed == "alt gr":
#         print("DETECTED")

#     else:
#         print(pressed)
