import uasyncio as asyncio

from misc import _free

container = dict()
config = dict()
modules_enabled = []

CONFIG_PATH = 'config.json'
MODULES_CONFIG_PATH = 'modules_enabled.json'
FORCED_MODULES = ['webserver', 'heartbeat', 'microconfig_web']


def _load_config():
    import ujson
    global config, modules_enabled

    def write(path, data):
        print('write', path, data)
        with open(path, 'w') as fh:
            fh.write(ujson.dumps(data))

    def load(path, default):
        try:
            with open(path, 'r') as fh:
                return ujson.loads(fh.read())
        except OSError as e:
            return default

    modules_enabled = load(MODULES_CONFIG_PATH, [])
    config = load(CONFIG_PATH, dict())

    print(modules_enabled, config)

    def get_module_default_config(module_name):
        global dirty, modules_enabled
        try:
            module = __import__(module_name)
            try:
                return module.get_default_config()
            except Exception as e:
                return dict()
        except ImportError:
            print('Module {} not exist'.format(name))
        except Exception:
            dirty = True
            modules_enabled.remove(module_name)

    dirty = False

    for forced_module in FORCED_MODULES:
        if forced_module not in modules_enabled:
            print('{} is forced -- enabling'.format(forced_module))
            modules_enabled.append(forced_module)
            dirty = True

    for name in modules_enabled:
        if not config.get(name):
            dirty = True
            config[name] = get_module_default_config(name)
            _free()

    if dirty:
        write(MODULES_CONFIG_PATH, modules_enabled)
        write(CONFIG_PATH, config)


def save_config(path, data):
    import ujson
    ujson.loads(data)  # ensure valid json

    with open(path, 'w') as fh:
        print('write', path, data)
        fh.write(data)


def init():
    print('Microconfig init')
    _load_config()
    loop = asyncio.PollEventLoop()

    for module in modules_enabled:
        _import_module(module)
        _free()

    _register()
    _boot(loop)
    _run(loop)


def _register():
    print('Registering...')
    for (name, module) in container.items():
        try:
            print('{} - register'.format(name))
            module.register(config.get(name, dict()))
            _free()
        except AttributeError:
            print('{} has no register()'.format(name))


def _boot(loop):
    print('Boot...')
    for (name, module) in container.items():
        try:
            print('{} - boot'.format(name))
            module.boot(container, loop)
            _free()
        except AttributeError as e:
            print('{} has no boot()'.format(name))
            print(e)


def _cleanup(loop):
    print('Cleanup')
    for (name, module) in container.items():
        try:
            print('{} - cleanup'.format(name))
            module.cleanup(container, loop)
            _free()
        except AttributeError as e:
            print('{} has no cleanup()'.format(name))
            print(e)
    loop.stop()


def _import_module(name):
    print('Loading module', name)
    try:
        module = __import__(name)
        _free()
        container[name] = module
    except Exception as e:
        print(e)


def _run(loop):
    print('Running...')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Interrupted')  # This mechanism doesn't work on Unix build.
    except MemoryError:
        import machine
        machine.reset()
    finally:
        _cleanup(loop)
