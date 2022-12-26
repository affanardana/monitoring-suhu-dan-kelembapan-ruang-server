from paho.mqtt import client as mqtt_client
from fuzzywuzzy import fuzz
import random
import time
import sqlite3
import json


broker = "localhost"
port = 1883
topic1 = "iot/sensor1"
topic2 = "iot/sensor2"
topic3 = "iot/sensor3"
topic4 = "iot/sensor4"
topic5 = "iot/sensor5"
client_id = f'python-mqtt-{random.randint(0, 100)}'

# Menentukan variabel fuzzy
temperature_low = 25
temperature_medium = (25, 35)
temperature_high = 35
humidity_low = 25
humidity_medium = (25, 50)
humidity_high = 50

# Fungsi untuk menentukan kondisi 
def determine_weather(temp, humidity):
  if temp <= temperature_low and humidity <= humidity_low:
    return "Dingin dan kering"
  elif temp >= temperature_medium[0] and temp <= temperature_medium[1] and humidity <= humidity_low:
    return "Normal dan kering"
  elif temp >= temperature_high and humidity <= humidity_low:
    return "Panas dan kering"
  elif temp <= temperature_low and humidity >= humidity_medium[0] and humidity <= humidity_medium[1]:
    return "Dingin dan agak lembab"
  elif temp >= temperature_medium[0] and temp <= temperature_medium[1] and humidity >= humidity_medium[0] and humidity <= humidity_medium[1]:
    return "Normal dan agak lembab"
  elif temp >= temperature_high and humidity >= humidity_medium[0] and humidity <= humidity_medium[1]:
    return "Panas dan agak lembab"
  elif temp <= temperature_low and humidity >= humidity_high:
    return "Dingin dan lembab"
  elif temp >= temperature_medium[0] and temp <= temperature_medium[1] and humidity >= humidity_high:
    return "Normal dan lembab"
  elif temp >= temperature_high and humidity >= humidity_high:
    return "Panas dan lembab"
    

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


con = sqlite3.connect("D:/Kuliah/Mata Kuliah/Semester 5/Internet of Things/Praktikum/monitoring-suhu-dan-kelembapan-ruang-server/log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor1 = '''CREATE TABLE IF NOT EXISTS log_sensor1 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor1)
con.commit()

con = sqlite3.connect("D:/Kuliah/Mata Kuliah/Semester 5/Internet of Things/Praktikum/monitoring-suhu-dan-kelembapan-ruang-server/log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor2 = '''CREATE TABLE IF NOT EXISTS log_sensor2 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor2)
con.commit()

con = sqlite3.connect("D:/Kuliah/Mata Kuliah/Semester 5/Internet of Things/Praktikum/monitoring-suhu-dan-kelembapan-ruang-server/log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor3 = '''CREATE TABLE IF NOT EXISTS log_sensor3 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor3)
con.commit()

con = sqlite3.connect("D:/Kuliah/Mata Kuliah/Semester 5/Internet of Things/Praktikum/monitoring-suhu-dan-kelembapan-ruang-server/log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor4 = '''CREATE TABLE IF NOT EXISTS log_sensor4 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor4)
con.commit()

con = sqlite3.connect("D:/Kuliah/Mata Kuliah/Semester 5/Internet of Things/Praktikum/monitoring-suhu-dan-kelembapan-ruang-server/log_sensor.sqlite")
cur = con.cursor()
buat_tabel_log_sensor5 = '''CREATE TABLE IF NOT EXISTS log_sensor5 (
topic TEXT NOT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
lokasi TEXT NOT NULL,
suhu REAL NOT NULL,
kelembapan REAL NOT NULL);'''
cur.execute(buat_tabel_log_sensor5)
con.commit()

con = sqlite3.connect("D:/Kuliah/Mata Kuliah/Semester 5/Internet of Things/Praktikum/monitoring-suhu-dan-kelembapan-ruang-server/log_sensor.sqlite")
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
            print(determine_weather(tuple[0], tuple[1]))

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
    run()
