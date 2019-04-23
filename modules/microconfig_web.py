from microconfig import save_config, CONFIG_PATH, MODULES_CONFIG_PATH, _load_config
from modules.webserver import route, html_escape, async_template


def render_form(response):
    import microconfig
    import ujson

    response.content = async_template('views/microconfig.html',
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
