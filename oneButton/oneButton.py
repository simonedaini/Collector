import json
import keyboard
from tkinter import *
from PIL import ImageTk, Image
import math
import pyautogui
import requests

customers = []
customer_incidents = []


def createWindow():
    global customers
    global customer_incidents

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

    response = requests.get("http://127.0.0.1:5000/customer")
    customers = json.loads(response.text)
    customer_names = [x['name'] for x in customers]

    customer_variables = StringVar(root)
    customer_variables.set(customer_names[1])
    w = OptionMenu(root, customer_variables, *customer_names, command=customer_callback)
    w.pack()

    customer_callback(customer_names[1])
    incidents_dates = [x['datetime'] for x in customer_incidents]

    incident_variables = StringVar(root)
    if len(incidents_dates) == 0:
        incidents_dates.append("-")

    incident_variables.set(incidents_dates[0])
    w = OptionMenu(root, incident_variables, *incidents_dates)
    w.pack()

    root.mainloop()


def customer_callback(event):
    global customer_incidents
    global customers
    id = -1
    for customer in customers:
        if customer["name"] == event:
            id = customer["id"]
            print("found {}".format(id))

    response = requests.get("http://127.0.0.1:5000/incident/{}".format(id))
    customer_incidents = json.loads(response.text)
    print(customer_incidents)
    return customer_incidents



while True:
    pressed = keyboard.read_key()
    if pressed == "alt gr":
        createWindow()