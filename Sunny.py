from ctypes import *
import SunnyDLL


def Base64ToHexDump(B):
    """ 传入字节数组 或 字符串 """
    v = B
    if isinstance(B, bytes):
        pass
    else:
        if isinstance(B, str):
            v = B.encode('utf-8')
        else:
            print("您传入的参数不是 字节数组 或 字符串")
            exit(1)
    return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.HexDump(v, len(v)))


class SunnyNet:
    def __init__(self):
        """ 创建Sunny中间件对象,可创建多个 """
        self.UDPCallback = None
        self.WsCallback = None
        self.TcpCallback = None
        self.HttpCallback = None
        self.Context = SunnyDLL.DLLSunny.CreateSunnyNet()

    def __del__(self):
        """ 释放SunnyNet """
        SunnyDLL.DLLSunny.ReleaseSunnyNet(self.Context)

    def bind_port(self, port):
        if isinstance(port, int):
            SunnyDLL.DLLSunny.SunnyNetSetPort(self.Context, port)

    def start(self):
        """ 启动前先绑定端口 """
        return bool(SunnyDLL.DLLSunny.SunnyNetStart(self.Context))

    def close_ie_proxy(self):
        """ 取消已经设置的IE代理 """
        SunnyDLL.DLLSunny.SetIeProxy(self.Context, True)

    def stop_proxy(self):
        """ 停止中间件【停止的同时将会自动关闭IE代理】 """
        self.close_ie_proxy()
        SunnyDLL.DLLSunny.SunnyNetClose(self.Context)

    def bind_callback(self, http_callback, tcp_callback, ws_callback, udp_callback):
        """ 开启 身份验证模式 后 删除用户名 """
        self.HttpCallback = 0
        self.TcpCallback = 0
        self.WsCallback = 0
        self.UDPCallback = 0
        if callable(http_callback):
            self.HttpCallback = SunnyDLL.HttpCallback(http_callback)
        if callable(tcp_callback):
            self.TcpCallback = SunnyDLL.TcpCallback(tcp_callback)
        if callable(ws_callback):
            self.WsCallback = SunnyDLL.WsCallback(ws_callback)
        if callable(udp_callback):
            self.UDPCallback = SunnyDLL.UDPCallback(udp_callback)
        SunnyDLL.DLLSunny.SunnyNetSetCallback(self.Context, self.HttpCallback, self.TcpCallback, self.WsCallback, self.UDPCallback)

    def install_cert(self):
        """ 启动后调用,将中间件的证书安装到系统内 返回安装结果文本，若失败需要手动安装 """
        err = SunnyDLL.PointerToText(SunnyDLL.DLLSunny.SunnyNetInstallCert(self.Context))
        if "添加到存储" in err:
            return True
        if "已经在存储中" in err:
            return True
        return False

    def get_error_msg(self):
        """ 获取中间件启动时的错误信息 """
        return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.SunnyNetError(self.Context))

    def process_proxy_load_driver(self):
        """
        只允许一个中间件服务 加载驱动,使用前，请先启动Sunny中间件
        """
        return bool(SunnyDLL.DLLSunny.StartProcess(self.Context))

    def process_proxy_add_process(self, name):
        """
        添加指定的进程名进行捕获（某些捕获不到的进程建议重启目标进程）[需调用 启动进程代理 后生效]
        name = 进程名 例如 e.exe
        """
        if not isinstance(name, str):
            return
        SunnyDLL.DLLSunny.ProcessAddName(self.Context, create_string_buffer(name.encode("utf-8")))


def MessageIdToSunny(MessageId):
    if not isinstance(MessageId, int):
        print("MessageIdToSunny 传入参数错误")
        exit(0)
    return SunnyDLL.Sunny(MessageId)
