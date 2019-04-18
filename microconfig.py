import uasyncio as asyncio

container = dict()


def init(modules):
    print('Microconfig init')
    loop = asyncio.PollEventLoop()

    for module in modules:
        _import_module(module)

    _register()
    _boot(loop)
    _run(loop)


def _register():
    print('Registering...')
    for (name, module) in container.items():
        try:
            print('{} - register'.format(name))
            module.register()
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
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Interrupted')  # This mechanism doesn't work on Unix build.
    finally:
        _cleanup(loop)
