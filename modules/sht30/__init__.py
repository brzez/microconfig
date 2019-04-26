from modules.mqtt import publish
from modules.sht30.sht30 import SHT30
import uasyncio as asyncio

sensor = SHT30()

def get_default_config():
    return dict(check_interval=10)


check_interval = None


def register(config):
    global check_interval

    check_interval = config.get('check_interval')


def boot(loop):
    loop.create_task(tick())


async def tick():
    import machine
    while True:
        adc = machine.ADC(0)
        battery_voltage = (adc.read() / 1023.0) * 4.2
        temperature, humidity = sensor.measure()

        publish(b'bat_voltage', b'{}'.format(battery_voltage))
        publish(b'humidity', b'{}'.format(humidity))
        publish(b'temperature', b'{}'.format(temperature))

        check_interval = 10 * 60 * 1000

        print('going to sleep')
        await asyncio.sleep(2)
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, check_interval)
        machine.deepsleep()
