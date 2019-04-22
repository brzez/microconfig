import subprocess
import mpy_cross
import os

PORT = '/dev/ttyUSB0'
OUT_DIR = './build'

FILES = [
    ('main.py', 'main.mpy'),
    ('microconfig_web.py', 'microconfig_web.mpy'),
    ('microconfig.py', 'microconfig.mpy'),
    ('mqtt/__init__.py', './mqtt/__init__.mpy'),
    ('mqtt/umqttsimple.py', './mqtt/umqttsimple.mpy'),
    ('info.py', 'info.mpy'),
    ('heartbeat.py', 'heartbeat.mpy'),
    ('./webserver/__init__.py', './webserver/__init__.mpy'),
    ('./webserver/form.py', './webserver/form.mpy'),
    ('./webserver/unquote.py', './webserver/unquote.mpy'),
    ('views/microconfig.html', './views/microconfig.html'),
    ('misc.py', 'misc.mpy'),
    ('f.py', 'f.mpy'),
]


def cross_compile(file):
    print('cross_compile {}'.format(file))
    name, ext = os.path.splitext(file)
    out = os.path.join(OUT_DIR, name + '.mpy')

    try:
        os.makedirs(os.path.dirname(out))
    except FileExistsError:
        pass

    p = mpy_cross.run(file, '-o', out)
    p.wait()
    return out


def upload(file, destination):
    print('Uploading', file, destination)
    subprocess.call(['ampy', '-p', PORT, 'put', file, destination])


def main():
    try:
        os.makedirs(OUT_DIR)
    except FileExistsError:
        pass

    for file in FILES:
        if isinstance(file, str):
            path = file
            destination = file
        else:
            path, destination = file

        ext = os.path.splitext(path)[1]

        if ext == '.py':
            path = cross_compile(path)

        upload(path, destination)


main()
