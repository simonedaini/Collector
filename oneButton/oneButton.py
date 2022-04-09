import keyboard
from tkinter import *
from PIL import ImageTk, Image
import math
import pyautogui


def createWindow():
    root = Tk()
    root.title("asd")
    root.geometry("800x500")
    
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("1.jpg")
    pic = Image.open("1.jpg")
    height = 400
    width = math.floor(pic.width * height / pic.height)
    resized = pic.resize((width, height), Image.ANTIALIAS)
    new_pic = ImageTk.PhotoImage(resized)
    pic_label = Label(root, image=new_pic)
    pic_label.pack()

    

    root.mainloop()

while True:
    pressed = keyboard.read_key()
    if pressed == "alt gr":
        createWindow()