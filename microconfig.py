import uasyncio as asyncio

container = dict()
config = dict()
modules_enabled = []

CONFIG_PATH = 'config.json'
MODULES_CONFIG_PATH = 'modules_enabled.json'

"""
TODO:
config loading flow:

- load enabled modules
- load module config

- foreach module:
    check if exists in config
        if not:
            try to import it & .get_default_config
            save module conf to config
    

"""


def _load_config():
    import ujson
    global config, modules_enabled

    def load_json(path, default):
        try:
            with open(path, 'r') as fh:
                return ujson.loads(fh.read())
        except OSError as e:
            with open(path, 'w') as fh:
                fh.write(ujson.dumps(default))

            return default

    config = load_json(CONFIG_PATH, dict())
    modules_enabled = load_json(MODULES_CONFIG_PATH, [])


def save_config(path, data):
    import ujson
    ujson.loads(data)  # ensure valid json

    with open(path, 'w') as fh:
        fh.write(data)


def init():
    print('Microconfig init')
    _load_config()
    loop = asyncio.PollEventLoop()

    for module in ['webserver']:
        _import_module(module)

    _register()
    _boot(loop)
    _run(loop)


def _register():
    print('Registering...')
    for (name, module) in container.items():
        try:
            print('{} - register'.format(name))
            module.register(config.get(name, dict()))
        except AttributeError:
            print('{} has no register()'.format(name))


def _boot(loop):
    print('Boot...')
    for (name, module) in container.items():
        try:
            print('{} - boot'.format(name))
            module.boot(container, loop)
        except AttributeError as e:
            print('{} has no boot()'.format(name))
            print(e)


def _cleanup(loop):
    print('Cleanup')
    for (name, module) in container.items():
        try:
            print('{} - cleanup'.format(name))
            module.cleanup(container, loop)
        except AttributeError as e:
            print('{} has no cleanup()'.format(name))
            print(e)
    loop.stop()


def _import_module(name):
    print('Loading module', name)
    try:
        module = __import__(name)

        container[name] = module
    except Exception as e:
        print(e)


def _run(loop):
    print('Running...')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Interrupted')  # This mechanism doesn't work on Unix build.
    finally:
        _cleanup(loop)
