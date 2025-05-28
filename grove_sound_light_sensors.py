import time
import math
import socket
import json
import grovepi
import paho.mqtt.client as mqtt

MQTT_BROKER = "broker.mqttdashboard.com"
#MQTT_BROKER = "macbook-Pro-de-Remi.local"
MQTT_PORT = 1883
SOUND_SENSOR_TYPE = "grove_L358"
SOUND_TOPIC = "pemesa/sound"
LIGHT_SENSOR_TYPE = "grove_Light1.1"
LIGHT_TOPIC = "pemesa/light"
TEMP_HUM_SENSOR_TYPE ="grove_DHT11"
TEMP_TOPIC = "pemesa/temperature"
HUM_TOPIC = "pemesa/humidity"


# On utilise le nom d'hôte comme localisation
room_id = socket.gethostname()

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
mqttc.loop_start()

# Connect the Grove Sound Sensor to analog port A0
# SIG,NC,VCC,GND
sound_sensor = 0
# Connect the Grove Light Sensor to analog port A1
light_sensor = 1
# Connect the DHt sensor to port D7
dht_sensor = 7

grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(light_sensor,"INPUT")

timing = 5 # Averaging sound over 5 seconds
polling_interval = 100 # reading 10 times per second

while True:
        try:
                average = 0
                for i in range(timing * polling_interval):
                        # Read the sound level
                        sound_value = grovepi.analogRead(sound_sensor)
                        #print("sensor_value = %d" %sensor_value)
                        average = ((average * i) + sound_value) / (i + 1)
                        time.sleep(1 / polling_interval)
                        
                # Publish sound averaged over {timing} seconds
                sound_reading = {"room_id" : room_id, "sensor_type" : SOUND_SENSOR_TYPE, "sound" : math.trunc(average)}
                sound_payload = json.dumps(sound_reading, ensure_ascii=False)
                print(sound_payload)
                mqttc.publish(SOUND_TOPIC, sound_payload)
                
                # Publish light
                light_value = grovepi.analogRead(light_sensor)
                light_reading = {"room_id" : room_id, "sensor_type" : LIGHT_SENSOR_TYPE, "light" : light_value}
                light_payload = json.dumps(light_reading, ensure_ascii=False)
                print(light_payload)
                mqttc.publish(LIGHT_TOPIC, light_payload)
                
                # Get temperature and humidity
                [ temp_value,hum_value ] = grovepi.dht(dht_sensor,0)
                
                # Publish temperature
                temp_reading = {"room_id" : room_id, "sensor_type" : TEMP_HUM_SENSOR_TYPE, "temperature" : temp_value}
                temp_payload = json.dumps(temp_reading, ensure_ascii=False)
                print(temp_payload)
                mqttc.publish(TEMP_TOPIC, temp_payload)

                # Publish humidity
                hum_reading = {"room_id" : room_id, "sensor_type" : TEMP_HUM_SENSOR_TYPE, "humidity" : hum_value}
                hum_payload = json.dumps(hum_reading, ensure_ascii=False)
                print(hum_payload)
                mqttc.publish(HUM_TOPIC, hum_payload)               
        except Exception as error:
                print(f"Error : {error}")
                break
mqttc.loop_stop()

