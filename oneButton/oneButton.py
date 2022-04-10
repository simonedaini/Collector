from cProfile import label
import json
import keyboard
from tkinter import *
from PIL import ImageTk, Image
import math
import pyautogui
import requests

root = None
customers = []
customer_om = None
incident_om = None
incident_variable = None


def createWindow():
    global root
    global customers
    global customer_om
    global incident_om
    global incident_variable


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

    variable = StringVar()
    variable.set(customer_names[0])
    customer_om = OptionMenu(root, variable, *customer_names, command=customer_callback)
    customer_om.pack()

    id = None
    for customer in customers:
        if customer["name"] == customer_names[0]:
            id = customer["id"]

    response = requests.get("http://127.0.0.1:5000/incident/{}".format(id))
    incidents = json.loads(response.text)
    incidents_dates = [x['datetime'] for x in incidents]
    
    incident_variable = StringVar()
    if len(incidents) > 0:
        incident_variable.set(incidents_dates[0])
    else:
        incident_variable.set("-")
    incident_om = OptionMenu(root, incident_variable, *incidents_dates)
    incident_om.pack()
    
    root.mainloop()


def customer_callback(event):
    global incident_om
    incident_om["menu"].delete(0, "end")

    id = None
    for customer in customers:
        if customer["name"] == event:
            id = customer["id"]

    response = requests.get("http://127.0.0.1:5000/incident/{}".format(id))
    incidents = json.loads(response.text)
    incident_dates = [x['datetime'] for x in incidents]

    if len(incident_dates) == 0:
        incident_variable.set("-")
    else:
        incident_variable.set(incident_dates[0])
    
    for date in incident_dates:
        incident_om["menu"].add_command(label=date)


while True:
    pressed = keyboard.read_key()
    if pressed == "alt gr":
        createWindow()