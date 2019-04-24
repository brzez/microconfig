import subprocess
import mpy_cross
import os

PORT = '/dev/ttyUSB0'
OUT_DIR = './build'

FILES = [
    ('main.py', 'main.py'),
    ('microconfig.py', 'microconfig.mpy'),
    ('views/microconfig.html', './views/microconfig.html'),
    ('misc.py', 'misc.mpy'),
    ('f.py', 'f.mpy'),

    ('modules/ensure_net.py', 'modules/ensure_net.mpy'),
    ('modules/net_config.py', 'modules/net_config.mpy'),
    ('modules/mqtt/__init__.py', 'modules/mqtt/__init__.mpy'),
    ('modules/mqtt/umqttsimple.py', 'modules/mqtt/umqttsimple.mpy'),
    ('modules/microconfig_web.py', 'modules/microconfig_web.mpy'),
    ('modules/heartbeat.py', 'modules/heartbeat.mpy'),
    ('modules/webserver/__init__.py', 'modules/webserver/__init__.mpy'),
    ('modules/webserver/form.py', 'modules/webserver/form.mpy'),
    ('modules/webserver/unquote.py', 'modules/webserver/unquote.mpy'),

    ('modules/sht30/__init__.py', 'modules/sht30/__init__.mpy'),
    ('modules/sht30/sht30.py', 'modules/sht30/sht30.mpy'),
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
