from flask import Flask,render_template
from datetime import datetime,date
import socket


app = Flask(__name__)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.86.46',1234))

humidity = 0
temperature = 0
soil_moisture = ""
date_day = date.today()
time = datetime.now().strftime("%H:%M:%S")
count = 1;

@app.route("/")
def home():
    global humidity
    global temperature
    global soil_moisture
    global count
    global date_day
    global time
    while True:
        msg = s.recv(128)
        if msg:
            msg = msg.decode('utf8')
            print(msg)
            if "hum" in msg and "None" not in msg:
                humidity = msg.strip("hum")
            if "temp" in msg and "None" not in msg:
                temperature = msg.strip("temp")
            if "Dry" in msg or "Wet" in msg:
                soil_moisture = msg
            count += 1
            return render_template('BioLad.html',humidity=humidity,temperature=temperature,soil_moisture=soil_moisture,date=date,time=time)

@app.route("/home/")
def date_add():
    global humidity
    global temperature
    global soil_moisture
    global date_day
    global time
    date_day = date.today()
    time = datetime.now().strftime("%H:%M:%S")
    return render_template('BioLad.html', humidity=humidity, temperature=temperature, soil_moisture=soil_moisture,
                           date=date_day, time=time)

if __name__ == "__main__":
    app.run()

