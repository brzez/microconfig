import uselect as select
import uasyncio as asyncio

from unquote import unquote

try:
    import usocket as socket
except:
    import socket


def render_template(name, **kwargs):
    with open(name, 'r') as file:
        content = file.read()
        return content.format(**kwargs)


class Request:
    def __init__(self):
        self.method = None
        self.path = None
        self.data = None
        self.headers = dict()

    async def _parse_request_data(self, reader, length):
        data = (await reader.read(length)).decode()

        parsed = dict()

        for v in data.split('&'):
            key, value = v.split('=')

            parsed[key] = unquote(value).decode()

        return parsed

    def _parse_request_line(self, line):
        parsed = line.decode().lower().split(' ')
        # print(parsed)
        self.method = parsed[0]
        self.path = parsed[1]

    def _parse_header(self, header, cast, line):
        if header not in line:
            return None
        value = line[len(header) + 2: -2]

        if cast:
            value = cast(value)

        print('{} {}'.format(header, value))

        self.headers[header] = value
        return value

    async def parse(self, reader):
        self._parse_request_line(await reader.readline())

        while True:
            line = await reader.readline()
            line = line.lower()

            if not line or line == b'\r\n':
                break

            self._parse_header('content-type', None, line) or \
            self._parse_header('content-length', int, line)

        data_length = self.headers.get('content-length')
        if data_length:
            self.data = await self._parse_request_data(reader, data_length)


class Response:
    def __init__(self, content=None):
        self.content = content

    async def write(self, writer):
        await writer.awrite(b'HTTP/1.1 200 OK\n')
        await writer.awrite(b'Content-Type: text/html\n')
        await writer.awrite(b'Connection: close\n\n')
        if self.content:
            await writer.awrite(self.content)


class Route:
    def __init__(self, path, method, f):
        self.path = path
        self.method = method
        self.f = f


class Router:
    def __init__(self):
        self.routes = []

    def register(self, path, method, f):
        self.routes.append(Route(path, method, f))

    def find_route_for_request(self, request):
        for route in self.routes:
            if route.path == request.path and (route.method == request.method or route.method is None):
                return route
        return None

    def handle(self, request, response):
        route = self.find_route_for_request(request)

        if not route:
            return False

        route.f(request, response)

        return True


class WebServer:
    def __init__(self):
        self.server_socket = None
        self.socks = []
        self.router = Router()
        self.poller = select.poll()

    async def run(self, loop, port=80):
        addr = socket.getaddrinfo('0.0.0.0', port, 0, socket.SOCK_STREAM)[0][-1]
        print('init sock')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(addr)
        server_socket.listen(5)

        self.server_socket = server_socket
        self.socks = [server_socket]

        print('Awaiting connection on port', port)
        self.poller.register(server_socket, select.POLLIN)
        while True:
            res = self.poller.poll(1)
            if res:
                try:
                    client_socket, addr = server_socket.accept()
                    print('{} connected'.format(addr))
                    loop.create_task(self.handle_client(client_socket))
                except OSError as e:
                    print(e)

            await asyncio.sleep_ms(200)

    async def handle_client(self, client_socket):
        self.socks.append(client_socket)
        reader = asyncio.StreamReader(client_socket)
        writer = asyncio.StreamWriter(client_socket, {})

        try:
            request = Request()

            await request.parse(reader)

            response = Response(content='404')

            self.router.handle(request, response)

            await response.write(writer)

        except OSError:
            pass

        # wait some time to prevent connection reset
        await asyncio.sleep(1)

        client_socket.close()
        self.socks.remove(client_socket)

    def close(self):
        self.poller.unregister(self.server_socket)
        print('Closing {} sockets.'.format(len(self.socks)))
        for sock in self.socks:
            sock.close()


server = WebServer()


def route(path, method=None):
    def wrap(f):
        server.router.register(path, method, f)

    return wrap


def redirect(path):
    return '<script>window.location="{}"</script>'.format(path)


def runserver():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(server.run(loop))
    except KeyboardInterrupt:
        print('Interrupted')  # This mechanism doesn't work on Unix build.
    finally:
        server.close()
