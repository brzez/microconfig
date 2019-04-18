import uasyncio as asyncio
from sys import platform


async def heartbeat(tms):
    if platform == 'pyboard':  # V1.x or D series
        from pyb import LED
        led = LED(1)
    elif platform == 'esp8266':
        from machine import Pin
        led = Pin(2, Pin.OUT, value=1)
    elif platform == 'linux':
        return  # No LED
    else:
        raise OSError('Unsupported platform.')
    while True:
        if platform == 'pyboard':
            led.toggle()
        elif platform == 'esp8266':
            led(not led())
        await asyncio.sleep_ms(tms)


def boot(container, loop):
    loop.create_task(heartbeat(1000))

