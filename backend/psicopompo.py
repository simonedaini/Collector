import keyboard
import tkinter as tk



while True:
    pressed = keyboard.read_key()
    if pressed == "alt gr":
        window = tk.Tk()
        label = tk.Label(text="Time")
        label.pack()
        time = tk.Entry()
        time.pack()
        button = tk.Button(text="Insert")
        button.pack()

        window.mainloop()

    else:
        print(pressed)
