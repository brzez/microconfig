from mqtt.umqttsimple import MQTTClient
mqtt_client = None


def register(config):
    import machine
    import ubinascii
    global mqtt_client
    mqtt_client = MQTTClient(ubinascii.hexlify(machine.unique_id()), config.get('server'), **config.get('kwargs'))


def get_default_config():
    return dict(
        server='localhost',
        kwargs=dict(
            user='user',
            password='pass'
        )
    )
