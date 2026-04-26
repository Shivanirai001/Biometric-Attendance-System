import cv2
import requests
from tkinter import *
from tkinter import simpledialog

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def check_ble():
    return "CLASSROOM"

def capture_face():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Camera not working")
        return False

    detected = False

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            detected = True
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow("Camera - Press S", frame)

        if cv2.waitKey(1) == ord('s'):
            break

    cam.release()
    cv2.destroyAllWindows()

    return detected

def fingerprint_auth():
    entered = simpledialog.askstring("Fingerprint","Enter PIN again", show='*')
    return entered == entry_pin.get()

def mark_face():
    pin = entry_pin.get()
    location = check_ble()

    if capture_face():
        res = requests.post("http://127.0.0.1:5000/login", json={"pin":pin,"location":location})
        status.set(res.json()["message"])
    else:
        status.set("Face not detected")

def mark_fingerprint():
    pin = entry_pin.get()
    location = check_ble()

    if fingerprint_auth():
        res = requests.post("http://127.0.0.1:5000/login", json={"pin":pin,"location":location})
        status.set(res.json()["message"])
    else:
        status.set("Fingerprint failed")

root = Tk()
root.title("ERP Biometric Attendance")
root.geometry("400x300")

Label(root,text="Enter PIN").pack()
entry_pin = Entry(root, show="*")
entry_pin.pack()

Button(root,text="Face Authentication",command=mark_face).pack(pady=10)
Button(root,text="Fingerprint Authentication",command=mark_fingerprint).pack(pady=10)

status = StringVar()
Label(root,textvariable=status).pack()

root.mainloop()