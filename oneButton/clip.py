from time import sleep
from pynput import keyboard, mouse
import os


press = []
screen = False

def on_press(key):
    global screen
    try:
        press.append(key.char)
    except AttributeError:
        press.append(key)

    print(press)
    if keyboard.Key.shift in press and keyboard.Key.ctrl in press and "*" in press:
        screen = True


def on_release(key):
    global screen
    try:
        k = key.char
        if k in press:
            press.remove(k)
    except:
        if key in press:
            press.remove(key)

def on_mouse_click(x, y, button, pressed):
    global screen
    if screen == True and pressed == False:
        sleep(1)
        print("Screen taken in the clipboard, saving to 1.png")
        os.system("xclip -selection clipboard -t image/png -o > '1.png'")
        screen = False

# Collect events until released
keyboard_listener =  keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener =  mouse.Listener(on_click=on_mouse_click)
keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()
