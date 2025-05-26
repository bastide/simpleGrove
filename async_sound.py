import asyncio
import json
import grovepi

SOUND_SENSOR_TYPE = "grove_L358"
SOUND_TOPIC = "pemesa/sound"
SOUND_TIMEOUT = 5 # Averaging sound over 5 seconds
polling_interval = 100 # reading 10 times per second
sound_sensor = 0

async def sound_sensor(client, room_id, shutdown_event):
	print("async_sound.py (async)") 
	while not shutdown_event.is_set():
		try:
			"""			
			average = 0
			for i in range(TIMEOUT * polling_interval):
				# Read the sound level
				sensor_value = grovepi.analogRead(sound_sensor)
				print(f"sound {sensor_value}")
				average = ((average * i) + sensor_value) / (i + 1)
				print(f"average {average}")
				await asyncio.sleep(1 / polling_interval)
			"""
			average = grovepi.analogRead(sound_sensor)
			sound_reading = {"room_id" : room_id, "sensor_type" : SOUND_SENSOR_TYPE, "sound" : average}
			sound_payload = json.dumps(sound_reading, ensure_ascii=False)
			print(sound_payload)
			await client.publish(SOUND_TOPIC, sound_payload)
			await asyncio.sleep(SOUND_TIMEOUT)
		except Exception as e:
			print(e)

