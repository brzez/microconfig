from microconfig import init
from modules.mqtt import subscribe
from modules.webserver import route


def test():
    init()


@subscribe('foo')
def asd(message):
    print('message from topic {}'.format(message))


@subscribe('bar')
def basd(message):
    print('message from topic {}'.format(message))


@route('/foo')
def foo(request, response):
    response.content = 'foo'


test()
