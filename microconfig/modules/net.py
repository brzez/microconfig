import uasyncio as asyncio

config = None


def get_default_config():
    return dict(reconnect=False, ssid=None, password=None)


def register(_config):
    import network

    global config
    config = _config

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    from time import sleep
    tries = 10
    while not sta_if.isconnected() and tries > 0:
        sleep(1)
        tries -= 1

    if sta_if.isconnected():
        print('Network connected', sta_if.ifconfig())
        ap_if.active(False)
    else:
        ap_if.active(True)
        print('AP active')


async def tick():
    import network
    sta_if = network.WLAN(network.STA_IF)
    while True:
        if not sta_if.isconnected():
            print('no network')
            if config.get('reconnect', False):
                from microconfig import misc
                misc.do_connect(config['ssid'], config['password'])

        await asyncio.sleep(10)


def boot(loop):
    loop.create_task(tick())
