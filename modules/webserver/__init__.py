from misc import _free

routes = []


def accept_handler(conn):
    import modules.webserver.handle_request
    import sys
    client, addr = conn.accept()
    print('{} connected'.format(addr))
    modules.webserver.handle_request.handle_request(client, routes)
    client.close()
    _free()
    del modules.webserver.handle_request
    del sys.modules['modules.webserver.handle_request']
    _free()


async def runserver(loop):
    import socket
    global server_socket
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ai = socket.getaddrinfo("0.0.0.0", 80)
    addr = ai[0][4]

    server_socket.bind(addr)
    server_socket.listen(1)
    server_socket.setsockopt(socket.SOL_SOCKET, 20, accept_handler)


def boot(loop):
    loop.create_task(runserver(loop))


def cleanup(loop):
    global server_socket
    server_socket.close()
    server_socket = None


def route(path, method=None):
    def wrap(f):
        routes.append((path, method, f))

    return wrap
