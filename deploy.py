import subprocess
import mpy_cross
import os

PORT = '/dev/ttyUSB0'
OUT_DIR = './build'

FILES = [
    ('main.py', 'main.py'),
    ('microconfig/microconfig.py', 'microconfig/microconfig.mpy'),
    ('microconfig/views/microconfig.html', 'microconfig/./views/microconfig.html'),
    ('microconfig/views/form.html', 'microconfig/./views/form.html'),
    ('microconfig/misc.py', 'microconfig/misc.mpy'),
    ('microconfig/f.py', 'microconfig/f.mpy'),

    ('microconfig/modules/global.py', 'microconfig/modules/global.mpy'),
    ('microconfig/modules/net.py', 'microconfig/modules/net.mpy'),
    ('microconfig/modules/net_config.py', 'microconfig/modules/net_config.mpy'),
    ('microconfig/modules/mqtt/__init__.py', 'microconfig/modules/mqtt/__init__.mpy'),
    ('microconfig/modules/mqtt/umqttsimple.py', 'microconfig/modules/mqtt/umqttsimple.mpy'),
    ('microconfig/modules/microconfig_web.py', 'microconfig/modules/microconfig_web.mpy'),
    ('microconfig/modules/heartbeat.py', 'microconfig/modules/heartbeat.mpy'),
    ('microconfig/modules/webserver/__init__.py', 'microconfig/modules/webserver/__init__.mpy'),
    ('microconfig/modules/webserver/handle_request.py', 'microconfig/modules/webserver/handle_request.mpy'),
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


ensured_dirs = []


def ensure_dir_exists(path):
    global ensured_dirs
    current_path = ''
    for directory in os.path.dirname(path).split('/'):
        current_path = os.path.join(current_path, directory)
        if current_path in ensured_dirs:
            continue

        subprocess.call(['ampy', '-p', PORT, 'mkdir', current_path])

        ensured_dirs.append(current_path)


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

        ext = os.path.splitext(destination)[1]
        ensure_dir_exists(destination)

        if ext == '.mpy':
            path = cross_compile(path)

        upload(path, destination)


main()
