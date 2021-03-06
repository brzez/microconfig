import uasyncio as asyncio

from misc import _free

RESET_ON_EXCEPTION_WAIT = 10
CONFIG_PATH = 'config.json'
MODULES_CONFIG_PATH = 'modules_enabled.json'

FORCED_MODULES = [
    'modules.global',
    'modules.net',
    'modules.webserver',
    'modules.microconfig_web',
    'modules.mqtt',
]


def load_config():
    import ujson

    def _load_config(path, default):
        try:
            with open(path, 'r') as fh:
                return ujson.loads(fh.read())
        except OSError:
            return default
        except ValueError:
            return default

    def write_config(path, data):
        with open(path, 'w') as fh:
            fh.write(ujson.dumps(data))

    modules_enabled = _load_config(MODULES_CONFIG_PATH, [])
    config = _load_config(CONFIG_PATH, dict())

    modules_dirty = False
    config_dirty = False

    for forced_module in FORCED_MODULES:
        if forced_module not in modules_enabled:
            modules_enabled.append(forced_module)
            modules_dirty = True

    # validate modules
    for module in modules_enabled:
        try:
            import_module(module)
        except ImportError as e:
            print('Module {} invalid'.format(module))
            print(e)
            modules_enabled.remove(module)
            modules_dirty = True

    for module in modules_enabled:
        if module not in config:
            default_config = call_module_method(module, 'get_default_config')
            if default_config:
                config[module] = default_config
                config_dirty = True

    if config_dirty:
        write_config(CONFIG_PATH, config)
    if modules_dirty:
        write_config(MODULES_CONFIG_PATH, modules_enabled)

    return modules_enabled, config


def call_module_method(module, method, default=None, args=()):
    try:
        m = import_module(module)
        return getattr(m, method)(*args)
    except AttributeError as e:
        return default


def import_module(path):
    module = __import__(path)

    for segment in path.split('.')[1:]:
        module = getattr(module, segment)

    return module


def save_config(path, data):
    import ujson
    ujson.loads(data)  # ensure valid json

    with open(path, 'w') as fh:
        print('write', path, data)
        fh.write(data)


def init():
    print('Microconfig init')
    modules_enabled, config = load_config()
    _free()

    loop = asyncio.PollEventLoop()

    imported_modules = []

    print('Importing modules')
    for name in modules_enabled:
        imported_modules.append((name, import_module(name)))
        print('- {}'.format(name))
        _free()

    _register(imported_modules, config)
    _boot(imported_modules, loop)
    _free(verbose=True)
    _run(imported_modules, loop)


def _register(modules, config):
    print('Registering')
    for name, module in modules:
        print('- {}'.format(name))
        try:
            module.register(config.get(name, dict()))
            print('-- success')
            _free()
        except AttributeError:
            print('-- no register method')


def _boot(modules, loop):
    print('Boot')
    for name, module in modules:
        print('- {}'.format(name))
        try:
            module.boot(loop)
            print('-- success')
            _free()
        except AttributeError as e:
            print('-- no boot method')


def _cleanup(modules, loop):
    print('Cleanup')
    for name, module in modules:
        print('- {}'.format(name))
        try:
            module.cleanup(loop)
            print('-- success')
            _free()
        except AttributeError as e:
            print('-- no cleanup method')
    loop.stop()


def _run(modules, loop):
    print('Running')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Interrupted')  # This mechanism doesn't work on Unix build.
    except MemoryError:
        import machine
        machine.reset()
    except Exception as e:
        print(e, type(e))
        print('restarting in {}'.format(RESET_ON_EXCEPTION_WAIT))
        import time
        time.sleep(RESET_ON_EXCEPTION_WAIT)
    finally:
        _cleanup(modules, loop)
