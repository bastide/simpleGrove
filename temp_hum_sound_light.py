import asyncio
from bleak import BleakScanner
from aiomqtt import Client, MqttError
import logging
import json
import signal
import socket

# Seuil RSSI pour considérer une balise comme "proche" (en dBm)
RSSI_THRESHOLD = -70
# On utilise le nom d'hôte comme localisation
room_id = socket.gethostname()

async def scan_ble_proches(balises):
    try:
        # Scanner pendant 4 secondes
        devices = await BleakScanner.discover(timeout=4.0, return_adv=True)
        proches = []
        for device, adv_data in devices.values():
            # Vérifier si le RSSI est supérieur au seuil et si le nom de la balise est dans la liste
            # des balises à surveiller
            if adv_data.rssi > RSSI_THRESHOLD and balises.get(device.address) is not None:
                # Ajouter la balise à la liste des balises proches
                proches.append( {"room_id" : room_id, "person_id" : balises.get(device.address), "RSSI" : adv_data.rssi})
        return proches
    except Exception as e:
        print(f"Erreur lors du scan : {e}")
        return []

async def main():
    # Global flag to signal shutdown
    shutdown_event = asyncio.Event()
    
    def handle_signal(sig, frame):
        """Signal handler to initiate graceful shutdown."""
        print(f"\nReceived signal {sig}, initiating shutdown...")
        shutdown_event.set()

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_signal)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, handle_signal) # Handle termination signals
    
    balises = load_config()    
    print("Démarrage du scan des balises proches...")
    client = Client("broker.mqttdashboard.com", 1883, keepalive=60) 
    while not shutdown_event.is_set():
        try:
            async with client:
                proches = await scan_ble_proches(balises)
                if proches:
                    print(f"\nNombre de balises détectées : {len(proches)}")
                    for balise in proches:
                        payload = json.dumps(balise, ensure_ascii=False)
                        await client.publish("pemesa/proximity", payload)
                        print(balise)
                else:
                    print("\nAucune balise proche détectée.")
                print("Prochain scan dans 5 secondes...")
                await asyncio.sleep(5)
        except MqttError:
            print("Connection lost, reconnecting in 5 seconds")
            await asyncio.sleep(5)

def load_config():
    # Charger la configuration depuis un fichier JSON
    try:
        with open('beacons.json', 'r') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("Fichier de configuration non trouvé.")
        return {}
    except json.JSONDecodeError:
        print("Erreur lors du chargement du fichier de configuration.")
        return {}
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return {}
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du programme.")
