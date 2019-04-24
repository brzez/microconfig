from modules.webserver import route, async_template


def render_form(response):
    response.content = async_template('views/form.html',
                                      form="""
                                        <form method="post">
                                        <div>ssid</div>
                                        <div><input type="text" name="ssid"/></div>
                                        <div>password</div>
                                        <div><input type="text" name="password"/></div>
                                        <input type="submit">
                                        </form>
                                      """)


@route('/wifi', 'get')
def get_index(request, response):
    render_form(response)


@route('/wifi', 'post')
def post_index(request, response):
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(request.data.get('ssid'), request.data.get('password'))
    render_form(response)
