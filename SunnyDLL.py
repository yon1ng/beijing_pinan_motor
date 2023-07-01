import struct
import ctypes
from ctypes import *

__RuntimeEnvironment = struct.calcsize("P") * 8 == 64

try:
    if __RuntimeEnvironment:
        lib = CDLL("./Sunny64.dll")
        TcpCallback = CFUNCTYPE(None, c_int64, c_char_p, c_char_p, c_int64, c_int64, c_int64, c_int64, c_int64, c_int64)
        HttpCallback = CFUNCTYPE(None, c_int64, c_int64, c_int64, c_int64, c_char_p, c_char_p, c_char_p, c_int64)
        WsCallback = CFUNCTYPE(None, c_int64, c_int64, c_int64, c_int64, c_char_p, c_char_p, c_int64, c_int64)
        UDPCallback = CFUNCTYPE(None, c_int64, c_char_p, c_char_p, c_int64, c_int64, c_int64, c_int64)
    else:
        lib = CDLL("./Sunny.dll")
        TcpCallback = CFUNCTYPE(None, c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_int, c_int)
        HttpCallback = CFUNCTYPE(None, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_char_p, c_int)
        WsCallback = CFUNCTYPE(None, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_int, c_int)
        UDPCallback = CFUNCTYPE(None, c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int)
except:
    print("载入DLL失败,请检测DLL文件")
    exit(1)


class LibSunny:
    def __getattr__(self, name):
        func = getattr(lib, name)
        func.restype = ctypes.POINTER(ctypes.c_int)
        return func


DLLSunny = LibSunny()


def PtrToByte(ptr, skip, num):
    result_as_int = ctypes.cast(ptr, ctypes.c_void_p).value
    if result_as_int == None:
        return bytearray()
    result_as_int += skip
    new_result_ptr = ctypes.cast(result_as_int, ctypes.POINTER(ctypes.c_int))
    buffer = ctypes.create_string_buffer(num)
    ctypes.memmove(buffer, new_result_ptr, num)
    return buffer.raw


def PtrToInt(ptr):
    return ctypes.cast(ptr, ctypes.c_void_p).value


def PointerToText(ptr):
    if ptr == 0:
        return ""
    buff = b''
    i = 0
    while True:
        bs = PtrToByte(ptr, i, 1)
        i += 1
        if bs[0] == 0:
            break
        buff = buff + bs
    try:
        return buff.decode('utf-8')
    except:
        return buff.decode('gbk')


def PointerToBytes(ptr):
    if ptr == 0:
        return bytearray()
    lp = PtrToByte(ptr, 0, 8)
    if len(lp) != 8:
        return lp
    Lxp = PtrToInt(DLLSunny.BytesToInt(create_string_buffer(lp), 8))
    return PtrToByte(ptr, 8, Lxp)


class SunnyRequest:
    def __init__(self, _MessageId):
        self.MessageId = _MessageId

    def del_gzip_tag(self):
        DLLSunny.DelRequestHeader(self.MessageId, create_string_buffer("Accept-Encoding".encode("utf-8")))

    def get_header_all(self):
        return PointerToText(DLLSunny.GetRequestAllHeader(self.MessageId))

    def get_header_single(self, key):
        if not isinstance(key, str):
            return ""
        return PointerToText(
            DLLSunny.GetRequestHeader(self.MessageId, create_string_buffer(key.encode("utf-8"))))


class SunnyResponse:
    def __init__(self, _MessageId):
        self.MessageId = _MessageId


# http 操作类
class Sunny:
    request = None
    response = None
    requestClientIp = ""

    def __init__(self, MessageId):
        self.request = SunnyRequest(MessageId)
        self.response = SunnyResponse(MessageId)
        self.requestClientIp = PointerToText(DLLSunny.GetRequestClientIp(MessageId))
