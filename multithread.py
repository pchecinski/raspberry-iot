#!/usr/bin/python
import threading
import serial
import json
import time
import sys
import Adafruit_DHT
import pymongo
import requests 
import subprocess

from glob import glob
from datetime import datetime
from db import collection

if len(sys.argv) != 3:
    print("Podaj współrzędne GPS jako parametry!")
    exit()

thetime = datetime.now()

DHT_PIN = 4  # GPIO PIN
DHT_SENSOR = Adafruit_DHT.AM2302  # sensor type
LOOP_DELAY = 30  # seconds
API_URL = 'https://api.checinski.dev' # API ARMAG
LAT = sys.argv[1] 
LON = sys.argv[2]

print(f"AM2302 Reader started on {str(thetime)} on pin {str(DHT_PIN)}")

## Wątek czytający serial ##
port_name = glob("/dev/ttyACM*")[0]
ser = serial.Serial(
    port=port_name, baudrate = 9600, timeout=1,
    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS
)

lock = threading.Lock()
serial_data = {}
serial_run = True

class serialReadThread(threading.Thread):
    def run(self):
        global serial_data, serial_run

        while serial_run:
            line = ser.readline()
            data = line.strip().decode('utf-8')
        
            if data and 'pm' in data:
                lock.acquire()
                serial_data = json.loads(data)
                serial_data['time']=str(datetime.now())
                print(f"serial data: {str(serial_data)}")
                lock.release()

serialRead = serialReadThread()
serialRead.start()

## Główny wątek aplikacji ##
try:
    while True:
        time.sleep(LOOP_DELAY)

        humidity, temperature = Adafruit_DHT.read_retry(sensor=DHT_SENSOR, pin=DHT_PIN)
        #print('Date: ' + str(datetime.now()) +
        #      ' Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))


        r = requests.get(f"{API_URL}/{LAT}/{LON}")
        api_data = {}

        if r.status_code == 200:
            api_data = r.json()

        info = {
            "date": str(datetime.now()), 
            "weather": {
                "humidity": humidity, 
                "temperature": temperature, 
                "type": DHT_SENSOR,
            },
            #"air": serial_data,
            "api_data": api_data,
            "gps": {
                "lat": sys.argv[1],
                "lon": sys.argv[2]
            }
        }
        
        print(info)
        collection.insert_one(info)

except (KeyboardInterrupt):
    serial_run = False
    print('Goodbye.')

except (pymongo.errors.AutoReconnect):
    print('Autoreconnect.')