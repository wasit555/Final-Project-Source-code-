# Final Project
# 2101524 Comp Prog 2022/2
# Wasit Khampeerapakorn 6230479321

# Press Restart 1-2 times after Run this code

import network
from machine import Pin, ADC
import dht
import urequests
import time

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Viking kak', '')

HTTP_HEADERS = {'Content-Type': 'application/json'}
THINGSPEAK_WRITE_API_KEY = ''

sensor = dht.DHT11(Pin(14))
ldr_pin = Pin(5, Pin.IN)
adc = ADC(0)

def measure_environment():
    sensor.measure()
    humidity = sensor.humidity()
    temperature = sensor.temperature()
    ldr_value = adc.read()
    return humidity, temperature, ldr_value

def convert_ldr_to_light(ldr_value):
    light_intensity = (1023 - ldr_value) / 1023.0 * 100.0
    return light_intensity

def send_data_to_thingspeak(humidity, temperature, light_intensity):
    sensor_readings = {
        'field1': '{:.1f}%'.format(humidity),
        'field2': '{:.1f} Celsius'.format(temperature),
        'field3': '{:.1f}%'.format(light_intensity)
    }
    request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json=sensor_readings, headers=HTTP_HEADERS)
    request.close()
    print(sensor_readings)

def run_measurement():
    while True:
        try:
            humidity, temperature, ldr_value = measure_environment()
            light_intensity = convert_ldr_to_light(ldr_value)
            send_data_to_thingspeak(humidity, temperature, light_intensity)
            time.sleep(0.5)
        except Exception as e:
            print("An error occurred:", e)
            print("Restarting...")
            time.sleep(1)
            continue

run_measurement()
