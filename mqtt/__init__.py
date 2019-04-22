import uasyncio as asyncio

from mqtt.umqttsimple import MQTTClient

mqtt_client = None
subscribes = []


def register(config):
    import machine
    import ubinascii
    global mqtt_client
    mqtt_client = MQTTClient(ubinascii.hexlify(machine.unique_id()), config.get('server'), **config.get('kwargs'))
    mqtt_client.set_callback(sub_cb)


def sub_cb(topic, msg):
    for sub_topic, f in subscribes:
        if topic == sub_topic:
            f(msg)


def boot(container, loop):
    try:
        mqtt_client.connect()
        print('mqtt connected')
        for (topic, f) in subscribes:
            mqtt_client.subscribe(topic)

        loop.create_task(tick())

    except Exception as e:
        print(e)


async def tick():
    while True:
        mqtt_client.check_msg()
        await asyncio.sleep(10)


def cleanup(container, loop):
    global mqtt_client

    if not mqtt_client:
        return

    mqtt_client.disconnect()
    mqtt_client = None


def get_default_config():
    return dict(
        server='localhost',
        kwargs=dict(
            user='user',
            password='pass'
        )
    )


def subscribe(topic):
    def wrap(f):
        if isinstance(topic, str):
            t = topic.encode()
        else:
            t = topic
        subscribes.append((t, f))

    return wrap
