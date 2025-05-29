import asyncio
import json
import grovepi

SOUND_SENSOR_TYPE = "grove_L358"
SOUND_TOPIC = "pemesa/sound"
SOUND_TIMEOUT = 5 # Averaging sound over 5 seconds
polling_interval = 100 # reading 10 times per second
sound_sensor = 0

def read_sound():
	try:
		sensor_value = grovepi.analogRead(sound_sensor)
		return sensor_value
	except Exception as e:
		print(f"Coud not read sound {e}")
		return 0
		
async def async_read_sound(loop):
	return await loop.run_in_executor(None, read_sound)
		
async def sound_sensor(client, room_id, shutdown_event):
	print("async_sound.py (async)") 
	loop = asyncio.get_running_loop()
	while not shutdown_event.is_set():
		try:
			average = 0
			for i in range(SOUND_TIMEOUT * polling_interval):
				# Read the sound level
				# sensor_value = grovepi.analogRead(sound_sensor)
				#sensor_value = await asyncio.to_thread(grovepi.analogRead, sound_sensor)
				#sensor_value = 12
				#print(f"sound {sensor_value}")
				sensor_value = await async_read_sound(loop)
				average = ((average * i) + sensor_value) / (i + 1)
				#print(f"average {average}")
				await asyncio.sleep(1 / polling_interval)

			sound_reading = {"room_id" : room_id, "sensor_type" : SOUND_SENSOR_TYPE, "sound" : average}
			sound_payload = json.dumps(sound_reading, ensure_ascii=False)
			print(sound_payload)
			await client.publish(SOUND_TOPIC, sound_payload)
			await asyncio.sleep(SOUND_TIMEOUT)
		except Exception as e:
			print(f"in while {e}")

