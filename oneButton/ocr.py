import pytesseract
import cv2
import re

image = cv2.imread("screenshot.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
text = pytesseract.image_to_string(image, config='--psm 11')

with open("ocr.txt", "w") as ocr:
    ocr.write(text)

ocr_datetime = re.findall(r"\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2}", text)
print("OCR Gathered datetimes = ".format(ocr_datetime))