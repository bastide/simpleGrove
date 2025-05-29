#!/usr/bin/env python

import asyncio
import time # Keep for initial sensor setup if needed, but use asyncio.sleep in loop
from datetime import datetime
from aiomqtt import Client, MqttError
import logging
import json
import signal
import socket
from async_sound import sound_sensor
from async_light import light_sensor
from async_temp_hum import temperature_humidity_sensor
from async_proximity import proximity_sensor



MQTT_BROKER = "broker.mqttdashboard.com"
#MQTT_BROKER = "macbook-Pro-de-Remi.local"
MQTT_PORT = 1883
# On utilise le nom d'hôte comme localisation
room_id = socket.gethostname()

# Global flag to signal shutdown
shutdown_event = asyncio.Event()

def handle_signal(sig, frame):
    """Signal handler to initiate graceful shutdown."""
    print(f"\nReceived signal {sig}, initiating shutdown...")
    shutdown_event.set()
    
async def main():
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_signal)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, handle_signal) # Handle termination signals
    
    # Use an 'async with' block for automatic cleanup
    async with Client(MQTT_BROKER, MQTT_PORT, keepalive=60) as client:
        shutdown_event.clear()
        await asyncio.gather(
            #sound_sensor(client, room_id, shutdown_event),
            #light_sensor(client, room_id, shutdown_event),
            #temperature_humidity_sensor(client, room_id, shutdown_event),
            proximity_sensor(client,room_id, shutdown_event),
            return_exceptions=True)  # Handle exceptions in tasks
    # The 'async with' block handles client.close() automatically


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # This might still catch the initial Ctrl+C if it happens before the loop starts
        print("\nShutdown requested (KeyboardInterrupt outside loop).")
    finally:
        print("Script finished.")

