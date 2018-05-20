import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11

def dht11(gpiopin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpiopin)

    if humidity is not None and temperature is not None:
        return {
            'temperature': temperature,
            'humidity': humidity
        }
