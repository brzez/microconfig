def handle_request(client, routes):
    method, path = client.readline().lower().split(b' ')[:2]

    print('{} {}'.format(method, path))
    content_type = None
    content_length = None

    while True:
        line = client.readline()

        if not line or line == b'\r\n':
            break

        if line.startswith(b'content-type'):
            content_type = line[14:]
        if line.startswith(b'content-length'):
            content_length = int(line[16:])

    print(method, path, content_type, content_length)
    data = None

    if content_length:
        data = parse_request_data(client.read(content_length))

    client.write(b'HTTP/1.1 200 OK\n')
    client.write(b'Content-Type: text/html\n')
    client.write(b'Connection: close\n\n')

    for _path, _method, f in routes:
        if method != _method and path != path:
            continue

        return f(client, data)

    client.write(b'404')


def parse_request_data(data):
    _data = {}
    for v in data.split(b'&'):
        key, value = v.split(b'=')
        _data[key] = _unquote_plus(value)
    return _data


def unquote(s):
    r = s.split('%')
    for i in range(1, len(r)):
        s = r[i]
        try:
            r[i] = chr(int(s[:2], 16)) + s[2:]
        except:
            r[i] = '%' + s
    return ''.join(r)


def _unquote_plus(s):
    return unquote(s.replace('+', ' '))
