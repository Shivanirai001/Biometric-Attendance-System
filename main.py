import cv2
import sqlite3
from tkinter import *

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, pin TEXT)")
conn.commit()

def capture_face():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():
        print("Camera not working")
        return False

    face_detected = False

    while True:
        ret, frame = cam.read()

        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face_detected = True
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow("Camera - Press S", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            break

    cam.release()
    cv2.destroyAllWindows()

    return face_detected

def register():
    name = entry_name.get()
    pin = entry_pin.get()

    if name == "" or pin == "":
        status.set("Enter name & PIN!")
        return

    if capture_face():
        cursor.execute("INSERT INTO users VALUES (?, ?)", (name, pin))
        conn.commit()
        status.set("Registered Successfully!")
    else:
        status.set("Face not detected!")

def login():
    pin = entry_pin.get()

    if pin == "":
        status.set("Enter PIN!")
        return

    if capture_face():
        cursor.execute("SELECT * FROM users WHERE pin=?", (pin,))
        user = cursor.fetchone()

        if user:
            status.set(f"Welcome {user[0]}!")
        else:
            status.set("Invalid Fingerprint/PIN!")
    else:
        status.set("Face not detected!")

root = Tk()
root.title("Biometric Authentication App")
root.geometry("400x350")

Label(root, text="Enter Name").pack()
entry_name = Entry(root)
entry_name.pack()

Label(root, text="Enter Fingerprint (PIN)").pack()
entry_pin = Entry(root, show="*")
entry_pin.pack()

Button(root, text="Register (Face + Fingerprint)", command=register).pack(pady=10)
Button(root, text="Login (Face + Fingerprint)", command=login).pack(pady=10)

status = StringVar()
Label(root, textvariable=status).pack()

root.mainloop()