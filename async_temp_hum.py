import asyncio
import json
import math
from grovepi import *

SENSOR_TYPE = "grove_DHT11"
TEMP_TOPIC = "pemesa/temperature"
HUM_TOPIC = "pemesa/humidity"
TIMEOUT = 5

dht_sensor_port = 7		# Connect the DHt sensor to port 7

async def temperature_humidity_sensor(client, room_id, shutdown_event):
	print("""async_tem_hum.py (async) """) 	
	while not shutdown_event.is_set():
		[ temp,hum ] = dht(dht_sensor_port,0)		#Get the temperature and Humidity from the DHT sensor
		if math.isnan(temp) == False:
			temp_reading = {"room_id" : room_id, "sensor_type" : SENSOR_TYPE, "temperature" : temp}
			temp_payload = json.dumps(temp_reading, ensure_ascii=False)
			await client.publish(TEMP_TOPIC, temp_payload)
		if math.isnan(hum) == False:
			hum_reading = {"room_id" : room_id, "sensor_type" : SENSOR_TYPE, "humidity" : hum}
			hum_payload = json.dumps(hum_reading, ensure_ascii=False)
			await client.publish(HUM_TOPIC, hum_payload)
		await asyncio.sleep(TIMEOUT)
