import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

_marker = []

class MCP3008Handler(object):

    def __init__(self, mapping=None):
        mapping = mapping or []
        self._by_port = {}
        self._by_name = {}
        for port, name, handler in mapping:
            self._by_port[port] = (name, handler)
            self._by_name[name] = (port, handler)


    def handle(self, data):
        result = {}
        for i,v in enumerate(data):
            name, handler = self._by_port.get(i, (None, None))
            if handler:
                result[name] = handler(v)
        return result

    def __call__(self, data):
        return self.handle(data)

SINGLETONS = {}

def mcp3008(spi_port=0, spi_device=0, sensor_mapping=[]):
    # sensor mapping is expected in this format
    # [ (index, name, handler), ... ]

    if sensor_mapping is _marker:
        sensor_mapping = []

    handler = MCP3008Handler(sensor_mapping)

    mcp = SINGLETONS.get((spi_port, spi_device), None)
    if mcp is None:
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spi_port, spi_device))
        SINGLETONS[(spi_port, spi_device)] = mcp
    
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    
    return (handler(values))
