# Final Project
# 2101524 Comp Prog 2022/2
# Wasit Khampeerapakorn 6230479321

# Press Restart 1-2 times after Run this code

import network
import machine
from machine import Pin, ADC
import dht
import urequests
import time

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Viking kak', 'Minecraft007')

HTTP_HEADERS = {'Content-Type': 'application/json'}
THINGSPEAK_WRITE_API_KEY = 'ZV4EP0VV8DCF3M8R'

sensor = dht.DHT11(Pin(14))
ldr_pin = Pin(5, Pin.IN)
adc = ADC(0)

# Measure temperature and humidity with DHT11 sensor, LDR sensor reading, and send the data to ThingSpeak
def measure_environment():
    sensor.measure()
    humidity = sensor.humidity()
    temperature = sensor.temperature()
    ldr_value = adc.read()
    return humidity, temperature, ldr_value

# Convert LDR reading to inverted light intensity value
def convert_ldr_to_light(ldr_value):
    inverted_value = 1023 - ldr_value
    # Adjust the conversion formula based on LDR characteristics (More light = More value in %)
    light_intensity = inverted_value / 1023.0 * 100.0
    return light_intensity

# Send sensor data to ThingSpeak
def send_data_to_thingspeak(humidity, temperature, light_intensity):
    sensor_readings = {
        'Humidity': '{:.1f}%'.format(humidity),
        'Temperature': '{:.1f} Celsius'.format(temperature),
        'Light Intensity': '{:.1f}%'.format(light_intensity)
    }
    request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json=sensor_readings, headers=HTTP_HEADERS)
    request.close()
    print("Sensor Readings:", sensor_readings)

while True:
    humidity, temperature, ldr_value = measure_environment()
    light_intensity = convert_ldr_to_light(ldr_value)
    send_data_to_thingspeak(humidity, temperature, light_intensity)
    time.sleep(0.5)
