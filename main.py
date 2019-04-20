from microconfig import init, save_config, CONFIG_PATH, MODULES_CONFIG_PATH, _load_config
from webserver import route, html_escape, render_template


def test():
    init()


def render_form(response):
    import microconfig
    import ujson

    response.content = render_template('views/microconfig.html',
                                       modules_enabled=html_escape(ujson.dumps(microconfig.modules_enabled)),
                                       config=html_escape(ujson.dumps(microconfig.config)))


@route('/', 'get')
def get_index(request, response):
    render_form(response)


@route('/', 'post')
def post_index(request, response):
    config = request.data.get('config')
    modules_enabled = request.data.get('modules_enabled')

    dirty = False
    if config:
        save_config(CONFIG_PATH, config)
        dirty = True
    if modules_enabled:
        save_config(MODULES_CONFIG_PATH, modules_enabled)
        dirty = True

    if dirty:
        _load_config()

    if request.data.get('command') == 'reboot':
        import machine
        machine.reset()

    render_form(response)


init()
# from webserver.form import form
# from webserver import redirect, route, render_template, runserver
#
# from machine import Pin
#
# d2 = Pin(4, Pin.OUT)
#
#
# @route('/')
# def get_index(request, response):
#     response.content = render_template('page.html')
#
#
# @route('/on')
# def get_on(request, response):
#     d2.value(1)
#     response.content = 'on' + redirect('/')
#
#
# @route('/off')
# def get_on(request, response):
#     d2.value(0)
#     response.content = 'off' + redirect('/')
#
#
# @form('/form', dict(
#     name=dict(type='text'),
#     password=dict(type='password'),
# ), 'form.html')
# def handle_form(data):
#     print('form', data)
