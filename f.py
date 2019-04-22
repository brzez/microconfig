import os

cwd = '.'


def rm(path, isdir):
    print('--- rm {}'.format(path))
    if isdir:
        for name, type, inode, size in os.ilistdir(path):
            isdir = True if type == 0x4000 else False
            rm('{}/{}'.format(path, name), isdir)
        os.rmdir(path)
    else:
        os.remove(path)


def l(command='ls'):
    global cwd
    index = 0

    command, *args = command.split(" ")

    if command == 'cd':
        cwd = args[0]

    for name, type, inode, size in os.ilistdir(cwd):
        index += 1
        isdir = True if type == 0x4000 else False

        full_path = '{}/{}'.format(cwd, name)

        if command == 'ls':
            print('{} {} {}'.format(index, 'd' if isdir else ' ', name))

        if command == 'rm' and str(index) in args and input('remove {}? y\\n\n'.format(full_path)) == 'y':
            rm(full_path, isdir)

    command = input('command (rm <file index> <file index>..., cd <abspath>):\n')
    l(command)
