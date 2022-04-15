from datetime import datetime
from email.mime import image
from time import sleep
from pynput import keyboard, mouse
import json
from pickletools import optimize
from tkinter import *
from PIL import ImageTk, Image, ImageGrab
from sys import platform

import math
import requests
import base64
import pytesseract
import cv2
import re
import os




root = None
customers = []
incidents = []
customer_om = None
incident_om = None
incident_variable = None
selected_customer = None
selected_incident = None
ocr_datetime = []
gather_datetime = []
image_name = "1.png"


def createWindow():
    global root
    global customers
    global incidents
    global customer_om
    global incident_om
    global incident_variable
    global selected_customer
    global selected_incident
    global ocr_datetime
    global gather_datetime

    root = Tk()
    root.title("asd")
    root.geometry("800x500")
    root.lift()

    pic = Image.open(image_name)

    height = 400
    width = math.floor(pic.width * height / pic.height)
    resized = pic.resize((width, height), Image.ANTIALIAS)
    new_pic = ImageTk.PhotoImage(resized)

    root.geometry("{}x{}".format(width, height + 200))

    pic_label = Label(root, image=new_pic)
    pic_label.grid(column=0, row=0, columnspan=10, rowspan=10)

    image = cv2.imread(image_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(image, config="--psm 11")

    with open("ocr.txt", "w") as ocr:
        ocr.write(text)

    ocr_datetime = re.findall(r"\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2}", text)
    

    try:
        response = requests.get("http://127.0.0.1:5000/customer")
        customers = json.loads(response.text)
        customer_names = [x['name'] for x in customers]

        variable = StringVar()
        variable.set(customer_names[0])
        selected_customer = customers[0]["id"]
        customer_om = OptionMenu(root, variable, *customer_names, command=customer_callback)
        customer_om.grid(row=11, column=0)

        id = None
        for customer in customers:
            if customer["name"] == customer_names[0]:
                id = customer["id"]
    
        try:
            response = requests.get("http://127.0.0.1:5000/customer/{}".format(id))
            incidents = json.loads(response.text)
        except:
            print("Server Unavailable 2")
       
        incidents_dates = [x['date'] for x in incidents]
        incident_variable = StringVar()
        if len(incidents) > 0:
            incident_variable.set(incidents_dates[0])
            selected_incident = incidents[0]["id"]
        else:
            incident_variable.set("-")
            incidents_dates = ["-"]
        incident_om = OptionMenu(root, incident_variable, *incidents_dates, command=incident_callback)
        incident_om.grid(row=11, column=1)

        datetime_label = Label(root, text="Datetime")
        datetime_label.grid(row=12, column=0)

        datetime_variable = StringVar()
        if len(ocr_datetime) > 0:
            datetime_variable.set(ocr_datetime[0])
        else:
            datetime_variable.set("-")
            ocr_datetime = ["-"]
        datetime_om = OptionMenu(root, datetime_variable, *ocr_datetime)
        datetime_om.grid(row=12, column=1)

    except:
        print("Server Unavailable")
    
    send_button = Button(root, text = "Send", command = send_callback)
    send_button.grid(row=13, column=0)

    root.mainloop()


def customer_callback(event):
    global incident_om
    global selected_customer
    global selected_incident

    incident_om["menu"].delete(0, "end")

    selected_customer = None
    for customer in customers:
        if customer["name"] == event:
            selected_customer = customer["id"]

    try:
        response = requests.get("http://127.0.0.1:5000/customer/{}".format(selected_customer))
        incidents = json.loads(response.text)
        incident_dates = [x['date'] for x in incidents]

        if len(incident_dates) == 0:
            incident_variable.set("-")
        else:
            selected_incident = incidents[0]["id"]
            incident_variable.set(incident_dates[0])
        
        for date in incident_dates:
            incident_om["menu"].add_command(label=date, command=lambda date=date: incident_callback(date))
    
    except:
        print("Server Unavailable")
    
    

def incident_callback(event):
    global selected_incident
    global incidents

    for incident in incidents:
        if incident["date"] == event:
            selected_incident = incident["id"]



def send_callback():
    global selected_incident
    global incidents
    global root
    global ocr

    try:
        with open(image_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf8")
    except:
        print("udable to open {}".format(image_name))  

    image_data = "data:image/{};base64,{}".format(image_name.split(".")[1], encoded_string)

    data = {
        "incidentId": selected_incident,
        "gather_datetime": str(datetime.now()),
        "datetime": str(datetime.now()),
        "killchain": "-",
        "host": "-",
        "host_type": "-",
        "image": image_data,
        "description": "-"
    }

    try:
        response = requests.post("http://127.0.0.1:5000/evidence/create", json=data)
    except:
        print("Server Unavailable {}".format(response.status_code))
    root.destroy()


# subprocess.run("xhost +")


press = []
screen = False

def on_press(key):
    global screen
    try:
        press.append(key.char)
    except AttributeError:
        press.append(key)

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

linux=True
windows=False

def on_mouse_click(x, y, button, pressed):
    global screen
    if screen == True and pressed == False:
        sleep(1)
        if platform != "win32":
            im = ImageGrab.grabclipboard()
            im.save('1.png','PNG')
        else:
            os.system("xclip -selection clipboard -t image/png -o > '1.png'")
        screen = False
        createWindow()

# Collect events until released
keyboard_listener =  keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener =  mouse.Listener(on_click=on_mouse_click)
keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()