import asyncio

async def light_sensor(mqtt, room_id, shutdown_event):
    print("""async_light.py (async) -""")
    while not shutdown_event.is_set():
        print("Light running");
        await asyncio.sleep(5)
