from modules.mqtt import subscribe
from machine import Pin, PWM

power_pin = Pin(5, Pin.OUT)
led_pin = Pin(4, Pin.OUT)
led_pwm = PWM(led_pin)


@subscribe(b'printer/power')
def power(msg):
    if msg == b'on':
        power_pin.value(1)

    if msg == b'off':
        power_pin.value(0)


@subscribe(b'printer/led')
def led(msg):
    try:
        value = int(msg)
        led_pwm.duty(value)
    except ValueError:
        pass
