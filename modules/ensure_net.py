def register(config):
    import network
    from time import sleep

    tries = 10
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    while not sta_if.isconnected() and tries > 0:
        sleep(1)
        tries -= 1

    if sta_if.isconnected():
        print('Network connected', sta_if.ifconfig())
        ap_if.active(False)
    else:
        ap_if.active(True)
        print('AP active')

