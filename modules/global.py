config = {}


def get_default_config():
    import ubinascii
    import machine
    return dict(name=ubinascii.hexlify(machine.unique_id()))


def register(_config):
    global config
    config.update(config)


def cleanup(*args):
    global config
    config = {}
