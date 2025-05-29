import json
from bleak import BleakScanner
from bleak.exc import BleakError
import asyncio

# Seuil RSSI pour considérer une balise comme "proche" (en dBm)
RSSI_THRESHOLD = -70
TIMEOUT = 10
TOPIC = "pemesa/proximity"

def load_config():
	# Charger la configuration depuis un fichier JSON
	try:
		with open('beacons.json', 'r') as f:
			config = json.load(f)
			return config
	except FileNotFoundError:
		print("Fichier de configuration des balises non trouve.")
		return {}
	except json.JSONDecodeError:
		print("Erreur lors du chargement du fichier de configuration.")
		return {}
	except Exception as e:
		print(f"Erreur inattendue : {e}")
		return {}

async def proximity_sensor(client, room_id, shutdown_event):
	print("async_proximity.py (async)")    
	balises = load_config()    
	print("Demarrage du scan des balises proches...")
	scanner = None
	while not shutdown_event.is_set():
		try:
			scanner = BleakScanner()
			await scanner.start()
			await asyncio.sleep(TIMEOUT)
			devices = await scanner.get_discovered_devices()
			await scanner.stop()
			if devices:
				print(f"{len(devices)} beacons found")
				for device in devices:
					# Verifier si le RSSI est superieur au seuil et si le nom de la balise est dans la liste
					# des balises a surveiller
					if device.rssi > RSSI_THRESHOLD and balises.get(device.address) is not None:
						balise = {"room_id" : room_id, "person_id" : balises.get(device.address), "RSSI" : device.rssi}
						payload = json.dumps(balise, ensure_ascii=False)
						print(f"Detected: {payload}")
						await client.publish(TOPIC, payload)
			else:
				print("No beacons found")
		except BleakError as e:
			print(f"Erreur lors du scan : {e}")                    
		print(f"Prochain scan dans {TIMEOUT / 2} secondes...")
		await asyncio.sleep(TIMEOUT)
		await scanner.stop()	

