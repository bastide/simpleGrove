import time
import grovepi

# Connect the Grove Sound Sensor to analog port A0
# SIG,NC,VCC,GND
sound_sensor = 0

grovepi.pinMode(sound_sensor,"INPUT")

from collections import deque

def real_time_running_average(window_size):
    """
    Generator for real-time running average of sensor readings.
    
    Args:
        window_size: Number of readings to include in the moving average
    
    Yields:
        Running average for each new reading
    """
    if window_size < 1:
        raise ValueError("Window size must be at least 1")
    
    window = deque(maxlen=window_size)
    
    while True:
        reading = yield
        window.append(reading)
        print("sum %d, len %d" % (sum(window) ,len(window)))
        yield sum(window) / len(window)

# Example usage with real-time data
def simulate_sensor():
    while True:
        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)
        yield sensor_value

# Initialize generator
avg_gen = real_time_running_average(window_size=3)
next(avg_gen)  # Prime the generator

# Simulate real-time readings
sensor = simulate_sensor()
averages = []
for reading in sensor:
    print("sensor_value = %d" %reading)
    time.sleep(.5)
    avg_gen.send(reading)
    print(next(avg_gen))
    #averages.append(round(next(avg_gen), 2))

print("Real-time running averages:", averages)
