#!/usr/bin/python3

import serial
import json
from datetime import datetime

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while True:
    line = ser.readline()
    data = line.strip().decode('utf-8')
    if data and 'pm' in data:
        json_data = json.loads(data)
        json_data['time']=str(datetime.now())
        str_data = str(json_data).replace("'", '"')

        with open('/home/pi/project/data/air-data.json', 'w') as f:
            f.write(str_data)
            print(str_data)
