from paho.mqtt import client as mqtt_client
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import random
import time
import sqlite3
import json
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image


broker = "localhost"
port = 1883
topic1 = "iot/sensor1"
topic2 = "iot/sensor2"
topic3 = "iot/sensor3"
topic4 = "iot/sensor4"
topic5 = "iot/sensor5"
client_id = f'python-mqtt-{random.randint(0, 100)}'

# New Antecedent/Consequent objects hold universe variables and membership
# functions
suhu = ctrl.Antecedent(np.arange(0,34,1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0,101,1), 'kelembapan')
kondisi = ctrl.Consequent(np.arange(0,11,1), 'kondisi')

# membuat variabel suhu dengan 3 fuzzy set
suhu['rendah'] = fuzz.trimf(suhu.universe, [0, 0, 18])
suhu['sedang'] = fuzz.trimf(suhu.universe, [13, 18, 23])
suhu['tinggi'] = fuzz.trimf(suhu.universe, [18, 33, 33])

# membuat variabel kelembapan dengan 3 fuzz set
kelembapan['rendah'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['tinggi'] = fuzz.trimf(kelembapan.universe, [50, 100, 100])

# membuat fuzzy set pada output kondisi
kondisi['buruk'] = fuzz.trimf(kondisi.universe, [0, 0, 5])
kondisi['lumayan baik'] = fuzz.trimf(kondisi.universe, [2, 5, 8])
kondisi['baik'] = fuzz.trimf(kondisi.universe, [5, 10, 10])


rule1 = ctrl.Rule(suhu['rendah'] & kelembapan['rendah'], kondisi['buruk'])
rule2 = ctrl.Rule(suhu['rendah'] & kelembapan['sedang'], kondisi['lumayan baik'])
rule3 = ctrl.Rule(suhu['rendah'] & kelembapan['tinggi'], kondisi['buruk'])
rule4 = ctrl.Rule(suhu['sedang'] & kelembapan['rendah'], kondisi['lumayan baik'])
rule5 = ctrl.Rule(suhu['sedang'] & kelembapan['sedang'], kondisi['baik'])
rule6 = ctrl.Rule(suhu['sedang'] & kelembapan['tinggi'], kondisi['lumayan baik'])
rule7 = ctrl.Rule(suhu['tinggi'] & kelembapan['rendah'], kondisi['buruk'])
rule8 = ctrl.Rule(suhu['tinggi'] & kelembapan['sedang'], kondisi['lumayan baik'])
rule9 = ctrl.Rule(suhu['tinggi'] & kelembapan['tinggi'], kondisi['buruk'])

kondisi_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
])

kondisi_fuzzy = ctrl.ControlSystemSimulation(kondisi_ctrl)



window = Tk()
window.title("MQTT Dashboard")
window.geometry('1130x600')  # Width, Height
window.resizable(False, False)  # Width, Height
window.configure(bg="white")

# suhu
# gambar suhu
rezizer = Image.open("suhu_img.png")
rezizer = rezizer.resize((50, 50))
rezizer.save("suhu_img_resized.png")

# kelembapan
# gambar kelembapan
rezizer = Image.open("hum_img.png")
rezizer = rezizer.resize((40, 40))
rezizer.save("hum_img_resized.png")

# gambar pemisah
rezizer = Image.open("pembatas.png")
rezizer = rezizer.resize((30, 600))
rezizer.save("pembatas_resized.png")

# kelembapan
# gambar kelembapan
rezizer = Image.open("hum_img.png")
rezizer = rezizer.resize((40, 40))
rezizer.save("hum_img_resized.png")

# box
# gambar box
rezizer = Image.open("box.png")
rezizer = rezizer.resize((210, 130))
rezizer.save("box_resized.png")

# textBox
# gambar textBox
rezizer = Image.open("textBox.png")
rezizer = rezizer.resize((340, 75))
rezizer.save("textBox_resized.png")

# boxInformation
# gambar boxInformation
rezizer = Image.open("boxInformation.png")
rezizer = rezizer.resize((340, 374))
rezizer.save("boxInformation_resized.png")


# baik
# gambar baik
rezizer = Image.open("baik.png")
rezizer = rezizer.resize((340, 75))
rezizer.save("baik_resized.png")


# lumayan_baik
# gambar lumayan_baik
rezizer = Image.open("lumayan_baik.png")
rezizer = rezizer.resize((340, 75))
rezizer.save("lumayan_baik_resized.png")


# buruk
# gambar buruk
rezizer = Image.open("buruk.png")
rezizer = rezizer.resize((340, 75))
rezizer.save("buruk_resized.png")

# circle
# gambar circle
rezizer = Image.open("circle.png")
rezizer = rezizer.resize((100, 107))
rezizer.save("circle_resized.png")

# background
# gambar background
rezizer = Image.open("background.png")
rezizer = rezizer.resize((1130, 600))
rezizer.save("background_resized.png")



img_suhu = PhotoImage(file="suhu_img_resized.png")
img_kelembaban = PhotoImage(file="hum_img_resized.png")
img_pembatas = PhotoImage(file = 'pembatas_resized.png')
img_box = PhotoImage(file = 'box_resized.png')
img_textBox = PhotoImage(file = 'textBox_resized.png')
img_background = PhotoImage(file = 'background_resized.png')
img_boxInformation = PhotoImage(file = 'boxInformation_resized.png')
img_baik = PhotoImage(file = 'baik_resized.png')
img_lumayan_baik = PhotoImage(file = 'lumayan_baik_resized.png')
img_buruk = PhotoImage(file = 'buruk_resized.png')
img_circle = PhotoImage(file = 'circle_resized.png')

# Menentukan variabel fuzzy
# temperature_low = (0,25)
# temperature_medium = (25, 35)
# temperature_high = (35, 50)
# humidity_low = 25
# humidity_medium = (25, 50)
# humidity_high = 50, 100

# Fungsi untuk menentukan kondisi 
# def determine_weather(temp, humidity):
#   if temp <= temperature_low and humidity <= humidity_low:
#     return "Dingin dan kering"
#   elif temp >= temperature_medium[0] and temp <= temperature_medium[1] and humidity <= humidity_low:
#     return "Normal dan kering"
#   elif temp >= temperature_high and humidity <= humidity_low:
#     return "Panas dan kering"
#   elif temp <= temperature_low and humidity >= humidity_medium[0] and humidity <= humidity_medium[1]:
#     return "Dingin dan agak lembab"
#   elif temp >= temperature_medium[0] and temp <= temperature_medium[1] and humidity >= humidity_medium[0] and humidity <= humidity_medium[1]:
#     return "Normal dan agak lembab"
#   elif temp >= temperature_high and humidity >= humidity_medium[0] and humidity <= humidity_medium[1]:
#     return "Panas dan agak lembab"
#   elif temp <= temperature_low and humidity >= humidity_high:
#     return "Dingin dan lembab"
#   elif temp >= temperature_medium[0] and temp <= temperature_medium[1] and humidity >= humidity_high:
#     return "Normal dan lembab"
#   elif temp >= temperature_high and humidity >= humidity_high:
#     return "Panas dan lembab"
    

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password) #auth service
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


con = sqlite3.connect("log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor1 = '''CREATE TABLE IF NOT EXISTS log_sensor1 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor1)
con.commit()

con = sqlite3.connect("log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor2 = '''CREATE TABLE IF NOT EXISTS log_sensor2 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor2)
con.commit()

con = sqlite3.connect("log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor3 = '''CREATE TABLE IF NOT EXISTS log_sensor3 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor3)
con.commit()

con = sqlite3.connect("log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor4 = '''CREATE TABLE IF NOT EXISTS log_sensor4 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor4)
con.commit()

con = sqlite3.connect("log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor5 = '''CREATE TABLE IF NOT EXISTS log_sensor5 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor5)
con.commit()

con = sqlite3.connect("log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_gabungan = '''CREATE TABLE IF NOT EXISTS log_mean (
mean_suhu bawah REAL NOT NULL,
mean_kelembapan REAL NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);'''
cur.execute(buat_tabel_log_gabungan)
con.commit()


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        
        print(f"Received {msg.payload.decode()} from {msg.topic} topic")
        data = json.loads(msg.payload.decode())
        topic = data['topic']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        lokasi = data['lokasi']
        suhu = data['suhu']
        kelembapan = data['kelembapan']
        
        con = sqlite3.connect("log_sensor.sqlite")
        cur = con.cursor()

        data_sensor_val = (topic, timestamp, lokasi, suhu, kelembapan)
        if (topic == topic1):
            cur.execute(
                "INSERT INTO log_sensor1 (topic, timestamp, lokasi, suhu, kelembapan) VALUES (?, ?, ?, ?, ?);", data_sensor_val)
            con.commit()
        elif (topic == topic2):
            cur.execute(
                "INSERT INTO log_sensor2 (topic, timestamp, lokasi, suhu, kelembapan) VALUES (?, ?, ?, ?, ?);", data_sensor_val)
            con.commit()
        elif (topic == topic3):
            cur.execute(
                "INSERT INTO log_sensor3 (topic, timestamp, lokasi, suhu, kelembapan) VALUES (?, ?, ?, ?, ?);", data_sensor_val)
            con.commit()
        elif (topic == topic4):
            cur.execute(
                "INSERT INTO log_sensor4 (topic, timestamp, lokasi, suhu, kelembapan) VALUES (?, ?, ?, ?, ?);", data_sensor_val)
            con.commit()
        elif (topic == topic5):
            cur.execute(
                "INSERT INTO log_sensor5 (topic, timestamp, lokasi, suhu, kelembapan) VALUES (?, ?, ?, ?, ?);", data_sensor_val)
            con.commit()
            cur.execute(
                """
                INSERT INTO log_mean (mean_suhu, mean_kelembapan) 
                VALUES (
                    ((select suhu from log_sensor1 order by timestamp DESC limit 1)+
                    (select suhu from log_sensor3 order by timestamp DESC limit 1)+ 
                    (select suhu from log_sensor4 order by timestamp DESC limit 1)+ 
                    (select suhu from log_sensor5 order by timestamp DESC limit 1)+ 
                    (select suhu from log_sensor2 order by timestamp DESC limit 1))/5, 
                    ((select kelembapan from log_sensor1 order by timestamp DESC limit 1)+
                    (select kelembapan from log_sensor2 order by timestamp DESC limit 1)+
                    (select kelembapan from log_sensor3 order by timestamp DESC limit 1)+
                    (select kelembapan from log_sensor4 order by timestamp DESC limit 1)+
                    (select kelembapan from log_sensor5 order by timestamp DESC limit 1))/5
                );""")
            con.commit()
            cur.execute("""
                select mean_suhu, mean_kelembapan from log_mean order by timestamp DESC limit 1
            """)
            con.commit()

            tuple = cur.fetchone()
            kondisi_fuzzy.input['suhu'] = tuple[0]
            kondisi_fuzzy.input['kelembapan'] = tuple[1]
            tsk = [(0,0),(0,0),(0,0),(0,0),(0,0)]
            for i in range(5):
                cur.execute("select suhu, kelembapan from log_sensor"+str(i+1)+" order by timestamp DESC limit 1")
                con.commit()
                tsk[i] = cur.fetchone()
            

                    

            # Crunch the numbers
            kondisi_fuzzy.compute()
            score = kondisi_fuzzy.output['kondisi']
            print(score)
            update_dashboard(tsk, score, tuple)

            if (score < 3.33):
                print('Kondisi ruangan buruk')
            elif (score < 6.67):
                print('kondisi ruangan lumayan baik')
            else:
                print('kondisi ruangan baik')
            

    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)
    client.subscribe(topic5)
    client.on_message = on_message

def create_dashboard():
    canvas_b = Canvas(window, bg='#aaaaaa', highlightthickness=0, width=1130, height=600)
    canvas_b.place(x=0, y=0)
    canvas_b.create_image(0, 0, anchor=NW, image = img_background)

    # sensor 1
    canvas_b.create_image(20, 440, anchor=NW, image = img_box)
    canvas_b.create_image(35, 460, anchor=NW, image=img_suhu)
    canvas_b.create_image(40, 510, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(90, 485, text='...'+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(87, 535, text='...'+" %", font=("Helvetica", 20), fill="white", anchor="w")

    # sensor 2
    canvas_b.create_image(500, 440, anchor=NW, image = img_box)
    canvas_b.create_image(515, 460, anchor=NW, image=img_suhu)
    canvas_b.create_image(520, 510, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(570, 480, text='...'+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(567, 535, text='...'+" %", font=("Helvetica", 20), fill="white", anchor="w")
    
    # sensor 3
    canvas_b.create_image(20, 30, anchor=NW, image = img_box)
    canvas_b.create_image(35, 50, anchor=NW, image=img_suhu)
    canvas_b.create_image(40, 100, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(90, 75, text='...'+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(87, 125, text='...'+" %", font=("Helvetica", 20), fill="white", anchor="w")

    # sensor 4
    canvas_b.create_image(500, 30, anchor=NW, image = img_box)
    canvas_b.create_image(515, 50, anchor=NW, image=img_suhu)
    canvas_b.create_image(520, 100, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(570, 70, text='...'+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(567, 120, text='...'+" %", font=("Helvetica", 20), fill="white", anchor="w")

    # sensor 5
    canvas_b.create_image(260, 235, anchor=NW, image = img_box)
    canvas_b.create_image(275, 255, anchor=NW, image=img_suhu)
    canvas_b.create_image(280, 305, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(325, 275, text='...'+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(322, 325, text='...'+" %", font=("Helvetica", 20), fill="white", anchor="w")

    canvas_b.create_image(730, 0, anchor=NW, image=img_pembatas)

    canvas_b.create_image(770, 10, anchor=NW, image=img_textBox)

    
    canvas_b.create_text(940, 65, text="Kondisi Ruangan", font=("Helvetica", 20), fill="white", anchor="s")
    
    canvas_b.create_image(770, 111, anchor=NW, image=img_baik)
    canvas_b.create_text(940, 166, text="...", font=("Helvetica", 20), fill="white", anchor="s")

    canvas_b.create_image(770, 206, anchor=NW, image=img_boxInformation)
    canvas_b.create_text(940, 236, text="Rata-rata", font=("Helvetica", 16), fill="white", anchor="s")
    
    
    canvas_b.create_image(822, 276, anchor=NW, image=img_circle)
    canvas_b.create_image(957, 276, anchor=NW, image=img_circle)
    canvas_b.create_image(847, 306, anchor=NW, image=img_suhu)
    canvas_b.create_image(987, 306, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(832, 416, text='...'+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(972, 416, text='...'+" %", font=("Helvetica", 20), fill="white", anchor="w")

    
    canvas_b.create_text(822, 526, text="Skor = "+'...', font=("Helvetica", 20), fill="white", anchor="w")

    

    


def update_dashboard(tsk, score, tskr):
    canvas_b = Canvas(window, bg='#aaaaaa', highlightthickness=0, width=1130, height=600)
    canvas_b.place(x=0, y=0)
    canvas_b.create_image(0, 0, anchor=NW, image = img_background)

    # sensor 1
    canvas_b.create_image(20, 440, anchor=NW, image = img_box)
    canvas_b.create_image(35, 460, anchor=NW, image=img_suhu)
    canvas_b.create_image(40, 510, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(90, 485, text=str(tsk[0][0])+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(87, 535, text=str(tsk[0][1])+" %", font=("Helvetica", 20), fill="white", anchor="w")

    # sensor 2
    canvas_b.create_image(500, 440, anchor=NW, image = img_box)
    canvas_b.create_image(515, 460, anchor=NW, image=img_suhu)
    canvas_b.create_image(520, 510, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(570, 480, text=str(tsk[1][0])+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(567, 535, text=str(tsk[1][1])+" %", font=("Helvetica", 20), fill="white", anchor="w")
    
    # sensor 3
    canvas_b.create_image(20, 30, anchor=NW, image = img_box)
    canvas_b.create_image(35, 50, anchor=NW, image=img_suhu)
    canvas_b.create_image(40, 100, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(90, 75, text=str(tsk[2][0])+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(87, 125, text=str(tsk[2][1])+" %", font=("Helvetica", 20), fill="white", anchor="w")

    # sensor 4
    canvas_b.create_image(500, 30, anchor=NW, image = img_box)
    canvas_b.create_image(515, 50, anchor=NW, image=img_suhu)
    canvas_b.create_image(520, 100, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(570, 70, text=str(tsk[3][0])+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(567, 120, text=str(tsk[3][1])+" %", font=("Helvetica", 20), fill="white", anchor="w")

    # sensor 5
    canvas_b.create_image(260, 235, anchor=NW, image = img_box)
    canvas_b.create_image(275, 255, anchor=NW, image=img_suhu)
    canvas_b.create_image(280, 305, anchor=NW, image=img_kelembaban)
    canvas_b.create_text(325, 275, text=str(tsk[4][0])+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(322, 325, text=str(tsk[4][1])+" %", font=("Helvetica", 20), fill="white", anchor="w")

    canvas_b.create_image(730, 0, anchor=NW, image=img_pembatas)

    canvas_b.create_image(770, 10, anchor=NW, image=img_textBox)

    
    canvas_b.create_text(940, 65, text="Kondisi Ruangan", font=("Helvetica", 20), fill="white", anchor="s")
    
    if (score < 3.33):
        canvas_b.create_image(770, 111, anchor=NW, image=img_buruk)
        canvas_b.create_text(940, 166, text="Buruk", font=("Helvetica", 20), fill="white", anchor="s")
    elif (score < 6.67):
        canvas_b.create_image(770, 111, anchor=NW, image=img_lumayan_baik)
        canvas_b.create_text(940, 166, text="Lumayan Baik", font=("Helvetica", 20), fill="white", anchor="s")
    else:
        canvas_b.create_image(770, 111, anchor=NW, image=img_baik)
        canvas_b.create_text(940, 166, text="Baik", font=("Helvetica", 20), fill="white", anchor="s")

    canvas_b.create_image(770, 206, anchor=NW, image=img_boxInformation)
    canvas_b.create_text(940, 236, text="Rata-rata", font=("Helvetica", 16), fill="white", anchor="s")
    
    canvas_b.create_image(822, 276, anchor=NW, image=img_circle)
    canvas_b.create_image(957, 276, anchor=NW, image=img_circle)
    canvas_b.create_image(847, 306, anchor=NW, image=img_suhu)
    canvas_b.create_image(987, 306, anchor=NW, image=img_kelembaban)
    
    canvas_b.create_text(832, 416, text=str(round(tskr[0],2))+" °C", font=("Helvetica", 20), fill="white", anchor="w")
    canvas_b.create_text(972, 416, text=str(round(tskr[1],2))+" %", font=("Helvetica", 20), fill="white", anchor="w")

    
    canvas_b.create_text(822, 526, text="Skor = "+str(round(score,2)), font=("Helvetica", 20), fill="white", anchor="w")



def run():
    client = connect_mqtt()
    subscribe(client)
    create_dashboard()
    client.loop_start()
    window.mainloop()
    client.loop_stop()

    


if __name__ == '__main__':
    # suhu.view()
    # kelembapan.view()
    # kondisi.view()
    # plt.show()


    run()


