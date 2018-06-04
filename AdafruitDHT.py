import sys
from time import sleep
import Adafruit_DHT
from DatabaseConnection import DatabaseConnection

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    s = 11
    p = 16

while True:
    humidity, temperature = Adafruit_DHT.read_retry(s, p)
    if humidity is not None and temperature is not None:
        values = DatabaseConnection.get_instance().database.Values
        values.insert_one({'id' : values.count(),  'temperature' : temperature, 'humidity' : humidity, 'pressure' : 0.5})
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    sleep(10)
