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
