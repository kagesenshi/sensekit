from sensekit.modules.mcp3008 import mcp3008
from sensekit.modules.dht11 import dht11
from sensekit.modules.sw420 import sw420
from sensekit.modules.bmp180 import bmp180
from sensekit.heat_idx import heat_idx
from multiprocessing import Process, Queue
from Queue import Empty as QueueEmpty
import RPi.GPIO as GPIO

import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(6, GPIO.IN)

def dht11reader(q):
    while True:
        q.put(dht11(21))


def sensor_reader(output):
    dht11output = dht11(21)
    dht11queue = Queue()
    dht11readerproc = Process(target=dht11reader, args=(dht11queue,))
    dht11readerproc.start()
    while True:
        d = {}
        try:
            dht11output = dht11queue.get(block=False)
        except QueueEmpty:
            pass

        d.update(mcp3008(0,0, [
            (7, 'illumination', lambda x: x), 
            (6, 'water-level', lambda x: x),
            (5, 'flame', lambda x: x),
            (4, 'smoke', lambda x: x),
            (3, 'carbon-monoxide', lambda x: x),
            (2, 'flammable-gas', lambda x: x),
            ]))
        d.update(bmp180())
        d.update({'humidity': dht11output['humidity']})
#        d.update(dht11output)
        d['motion'] = GPIO.input(6)
        d['timestamp'] = int(time.time() * 1000)
        d['heat-idx'] = heat_idx(d['temperature'],d['humidity'])
        output.put(d)

def stagger(q, seconds=1):
    start = time.time()
    data = []
    while (time.time() - start) < seconds or len(data) == 0:
        data.append(q.get())
    grouped = {}
    for d in data:
        for k,v in d.items():
            grouped.setdefault(k, [])
            grouped[k].append(v)
    result = {}
    for k, v in grouped.items():
        if k == 'timestamp':
            result[k] = max(v)
        else:
            result[k] = round(float(sum(v))/ len(v), 2)
    return result

if __name__ == '__main__':
    q = Queue()
    proc = Process(target=sensor_reader, args=(q,))
    proc.start()
    data = []
    while True:
        data = stagger(q, 1)
        print(data)
        
