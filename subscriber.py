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

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# buat tabel
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

            kondisi_fuzzy.compute()
            score = kondisi_fuzzy.output['kondisi']
            print(score)
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




def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    # dashboard
    window = Tk()
    window.title("MQTT Dashboard")
    window.geometry('500x440')  # Width, Height
    window.resizable(False, False)  # Width, Height
    window.configure(bg="white")
    window.mainloop()
    # suhu.view()
    # kelembapan.view()
    # kondisi.view()
    # plt.show()
    run()