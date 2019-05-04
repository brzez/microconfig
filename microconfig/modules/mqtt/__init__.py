import uasyncio as asyncio

from microconfig.modules.mqtt.umqttsimple import MQTTClient

mqtt_client = None
subscribes = []

config = None


def do_connect():
    import machine
    import ubinascii
    global mqtt_client
    client = MQTTClient(ubinascii.hexlify(machine.unique_id()), config.get('server'), **config.get('kwargs'))
    client.set_callback(sub_cb)

    client.connect()
    print('mqtt connected')
    for (topic, f) in subscribes:
        client.subscribe(topic)

    mqtt_client = client


def register(_config):
    global config

    config = _config
    try:
        do_connect()
    except OSError:
        pass


def sub_cb(topic, msg):
    for sub_topic, f in subscribes:
        if topic == sub_topic:
            f(msg)


def boot(loop):
    try:
        do_connect()
        loop.create_task(tick())

    except Exception as e:
        print(e)


async def tick():
    global mqtt_client

    while True:
        try:
            if mqtt_client is None:
                do_connect()
            else:
                mqtt_client.check_msg()
        except OSError as e:
            print(e, type(e))
            mqtt_client = None

        await asyncio.sleep(1)


def cleanup(loop):
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


def publish(topic, message):
    mqtt_client.publish(topic, message)


def subscribe(topic):
    def wrap(f):
        if isinstance(topic, str):
            t = topic.encode()
        else:
            t = topic
        subscribes.append((t, f))

    return wrap
