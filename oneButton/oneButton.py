from cProfile import label
from datetime import datetime
import json
from click import command
import keyboard
from tkinter import *
from PIL import ImageTk, Image
import math
import pyautogui
import requests
import base64

root = None
customers = []
incidents = []
customer_om = None
incident_om = None
incident_variable = None
selected_customer = None
selected_incident = None


def createWindow():
    global root
    global customers
    global incidents
    global customer_om
    global incident_om
    global incident_variable


    root = Tk()
    root.title("asd")
    root.geometry("800x500")
    
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("screenshot.jpg")
    pic = Image.open("screenshot.jpg")
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
    incident_om = OptionMenu(root, incident_variable, *incidents_dates, command=incident_callback)
    incident_om.pack()


    send_button = Button(root, text = "Hello", command = send_callback)
    send_button.pack()

    
    root.mainloop()



def customer_callback(event):
    global incident_om
    global selected_customer
    incident_om["menu"].delete(0, "end")

    selected_customer = None
    for customer in customers:
        if customer["name"] == event:
            selected_customer = customer["id"]

    response = requests.get("http://127.0.0.1:5000/incident/{}".format(selected_customer))
    incidents = json.loads(response.text)
    incident_dates = [x['datetime'] for x in incidents]

    if len(incident_dates) == 0:
        incident_variable.set("-")
    else:
        incident_variable.set(incident_dates[0])
    
    for date in incident_dates:
        incident_om["menu"].add_command(label=date, command=lambda date=date: incident_callback(date))
    

def incident_callback(event):
    global selected_incident
    global incidents

    for incident in incidents:
        if incident["datetime"] == event:
            selected_incident = incident["id"]



def send_callback():
    global selected_incident
    global incidents

    with open("screenshot.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    base64_image = str("data:image/jpeg;base64," + str(encoded_string))

    data = {
        "incidentId": 1,
        "datetime": str(datetime.now()),
        "killchain": "-",
        "host": "-",
        "host_type": "-",
        "image": base64_image,
        "description": "-"
    }

    data = json.dumps(data)
    print(str(base64_image)[:50])


    response = requests.post("http://127.0.0.1:5000/evidence/create", data=json.dumps(data))
    print(response.status_code)



while True:
    pressed = keyboard.read_key()
    if pressed == "alt gr":
        createWindow()