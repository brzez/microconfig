
def boot(*args):
    import network

    sta_if = network.WLAN(network.STA_IF)
    access_point_iface = network.WLAN(network.AP_IF)

    if sta_if.isconnected():
        print(sta_if.ifconfig())
    else:
        print('sta_if not connected')

    if access_point_iface.active():
        print(access_point_iface.ifconfig())
    else:
        print('access_point_iface not active')

