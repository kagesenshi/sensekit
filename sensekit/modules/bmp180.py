import Adafruit_BMP.BMP085 as BMP085

#def bmp180():
#    sensor = Sensor(0x77)
#    return {
#        'pressure': sensor.get_pressure()
#    }
#

GLOBAL={}

def bmp180(busnum=0):
    sensor = GLOBAL.get(busnum, None)
    if sensor is None:
        sensor = BMP085.BMP085(busnum)
        GLOBAL[busnum] = sensor

    return {
       'temperature': sensor.read_temperature(),
       'pressure': sensor.read_pressure(),
       'altitude': sensor.read_altitude(),
       'sealevel-pressure': sensor.read_sealevel_pressure(),
    }
