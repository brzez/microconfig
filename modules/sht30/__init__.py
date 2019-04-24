from modules.sht30.sht30 import SHT30

sensor = SHT30()

temperature, humidity = sensor.measure()

print('Temperature:', temperature, 'ºC, RH:', humidity, '%')