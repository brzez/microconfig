from modules.mqtt import publish
from modules.sht30.sht30 import SHT30
import uasyncio as asyncio

sensor = SHT30()

temperature, humidity = sensor.measure()

print('Temperature:', temperature, 'ºC, RH:', humidity, '%')


def get_default_config():
    return dict(check_interval=10)


check_interval = None


def register(config):
    global check_interval

    check_interval = config.get('check_interval')


def boot(loop):
    loop.create_task(tick())


async def tick():
    while True:
        temperature, humidity = sensor.measure()
        publish(b'humidity', b'{}'.format(humidity))
        publish(b'temperature', b'{}'.format(temperature))
        await asyncio.sleep(check_interval)
