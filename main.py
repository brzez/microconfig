from microconfig import init
from mqtt import subscribe
from webserver import route


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
