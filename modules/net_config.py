from modules.webserver import route, template


def render_form(client):
    template(client, 'views/form.html',
             form="""
                    <form method="post">
                    <div>ssid</div>
                    <div><input type="text" name="ssid"/></div>
                    <div>password</div>
                    <div><input type="text" name="password"/></div>
                    <input type="submit">
                    </form>
                  """)


@route(b'/wifi', b'get')
def get_index(client, data):
    render_form(client)


@route(b'/wifi', b'post')
def post_index(client, data):
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(data.get(b'ssid'), data.get(b'password'))
    render_form(client)
