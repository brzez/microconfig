import network

def do_connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def init():
    sta_if = network.WLAN(network.STA_IF)
    access_point_iface = network.WLAN(network.AP_IF)

    access_point_iface.config(password='1234567890')

    print(dict(
        sta_if=sta_if.active(),
        ap_if=access_point_iface.active()
    ))

    print(
        access_point_iface.config('mac'),
        access_point_iface.config('essid'),
        access_point_iface.config('channel'),
        access_point_iface.config('hidden'),
        access_point_iface.config('authmode'),
    )

    access_point_iface.ifconfig((
        '192.168.0.1',
        '255.255.255.0',
        '192.168.0.0',
        '8.8.8.8'
    ))

    print(access_point_iface.ifconfig())
    print(sta_if.active(), sta_if.ifconfig())

    access_point_iface.active(True)
