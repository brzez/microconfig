from microconfig import save_config, CONFIG_PATH, MODULES_CONFIG_PATH, load_config
from microconfig.modules.webserver import route, html_escape, template


def render_form(client):
    import ujson
    modules_enabled, config = load_config()

    template(client, 'views/microconfig.html',
             modules_enabled=html_escape(ujson.dumps(modules_enabled)),
             config=html_escape(ujson.dumps(config))
             )


@route(b'/', b'get')
def get_index(client, data):
    render_form(client)


@route(b'/', b'post')
def post_index(client, data):
    config = data.get(b'config')
    modules_enabled = data.get(b'modules_enabled')

    if config:
        save_config(CONFIG_PATH, config)
    if modules_enabled:
        save_config(MODULES_CONFIG_PATH, modules_enabled)

    if data.get(b'command') == b'reboot':
        import machine
        machine.reset()

    render_form(client)
