#!/usr/bin/env python
#
# GrovePi Example for using the Grove Sound Sensor and the Grove LED
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Modules:
#	 http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
#	 http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import socket
import json
import grovepi
import paho.mqtt.client as mqtt

#MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_BROKER = "macbook-Pro-de-Remi.local"
MQTT_PORT = 1883
SOUND_SENSOR_TYPE = "grove_L358"
SOUND_TOPIC = "pemesa/sound"

# On utilise le nom d'hôte comme localisation
room_id = socket.gethostname()

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
mqttc.loop_start()

# Connect the Grove Sound Sensor to analog port A0
# SIG,NC,VCC,GND
sound_sensor = 0

grovepi.pinMode(sound_sensor,"INPUT")

timing = 5 # Averaging sound over 5 seconds
polling_interval = 100 # reading 10 times per second

while True:
        try:
                average = 0
                for i in range(timing * polling_interval):
                        # Read the sound level
                        sensor_value = grovepi.analogRead(sound_sensor)
                        #print("sensor_value = %d" %sensor_value)
                        average = ((average * i) + sensor_value) / (i + 1)
                        time.sleep(1 / polling_interval)
                sound_reading = {"room_id" : room_id, "sensor_type" : SOUND_SENSOR_TYPE, "sound" : average}
                sound_payload = json.dumps(sound_reading, ensure_ascii=False)
                print(sound_payload)
                mqttc.publish(SOUND_TOPIC, sound_payload)
        except Exception as error:
                print(f"Error : {error}")
                break
mqttc.loop_stop()

