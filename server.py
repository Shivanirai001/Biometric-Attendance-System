from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS attendance")
cursor.execute("DROP TABLE IF EXISTS timetable")

cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pin TEXT, enrollment TEXT)")
cursor.execute("CREATE TABLE attendance (name TEXT, enrollment TEXT, subject TEXT, time TEXT, day TEXT)")
cursor.execute("CREATE TABLE timetable (day TEXT, hour INTEGER, subject TEXT)")

students = [
("Shivani Rai","1111","230160203014"),
("Adya Sabarwal","2222","230160203015"),
("Ajay","3333","230160203016"),
("Kiyosha","4444","230160203017"),
("Anya","5555","230160203018"),
("Shannon","6666","230160203019"),
("Prerna","7777","230160203020"),
("Luv","8888","230160203021"),
("Vansh","9999","230160203022"),
("Ashu","1010","230160203023")
]

cursor.executemany("INSERT INTO students (name,pin,enrollment) VALUES (?,?,?)", students)

timetable = [
("Monday",1,"CSE3047"),("Monday",2,"TRA2501"),("Monday",3,"CSE3745"),
("Tuesday",2,"CSE3745"),("Tuesday",3,"TRA2501"),("Tuesday",4,"CSE3013"),
("Wednesday",3,"CSE3047"),("Wednesday",4,"CSE3745"),("Wednesday",5,"CSE3013"),("Wednesday",6,"ENP2763"),
("Thursday",1,"CSE3745"),("Thursday",3,"CSE3013"),("Thursday",5,"CSE3013L"),
("Friday",1,"CSE3047"),("Friday",3,"CSE3047L")
]

cursor.executemany("INSERT INTO timetable VALUES (?,?,?)", timetable)
conn.commit()

def get_subject():
    now = datetime.datetime.now()
    day = now.strftime("%A")
    hour = now.hour

    slot = 0
    if 9 <= hour < 10: slot = 1
    elif 10 <= hour < 11: slot = 2
    elif 11 <= hour < 12: slot = 3
    elif 12 <= hour < 13: slot = 4
    elif 13 <= hour < 14: slot = 5
    elif 14 <= hour < 15: slot = 6

    cursor.execute("SELECT subject FROM timetable WHERE day=? AND hour=?", (day,slot))
    result = cursor.fetchone()

    if result:
        return result[0]
    return "No Class"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    pin = data['pin']
    location = data['location']

    if location != "CLASSROOM":
        return jsonify({"message": "Not in classroom"})

    cursor.execute("SELECT * FROM students WHERE pin=?", (pin,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid student"})

    subject = get_subject()
    time = str(datetime.datetime.now())
    day = datetime.datetime.now().strftime("%A")

    cursor.execute("INSERT INTO attendance VALUES (?,?,?,?,?)", (user[1],user[3],subject,time,day))
    conn.commit()

    return jsonify({"message": f"{user[1]} ({user[3]}) marked present in {subject}"})

@app.route('/attendance', methods=['GET'])
def attendance():
    cursor.execute("SELECT * FROM attendance")
    return jsonify(cursor.fetchall())

app.run(host='0.0.0.0', port=5000)