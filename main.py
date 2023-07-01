# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @Site    : 平安傻瓜式预约抢号
# @Software: PyCharm
import json
import time

import requests

import Sunny as SyNet


def BytesToStr(b):
    try:
        return b.decode('utf-8')
    except:
        return b.decode('gbk')


class Callback:
    Http_message_request_start = 1
    Http_message_request_success = 2
    Http_message_request_fail = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
    }
    timestamp = int(time.time() * 1000)
    sessionId = ''
    signature = ''
    url = 'https://newretail.pingan.com.cn/ydt/reserve/store/bookingTime?storefrontseq=39807&businessType=14&time={}'.format(
        timestamp)

    def booking(date, start_time, end_time, id_booking_survey):
        # 预约接口
        booking_url = 'https://newretail.pingan.com.cn/ydt/reserve/reserveOffline?time={}'.format(Callback.timestamp)
        body = {
            "businessName": "承保验车",
            "storefrontName": "摩托车投保预约",
            "bookingDate": date,
            "bookingTime": start_time + '-' + end_time,
            "bookingType": "1",
            "storefrontseq": "39807",
            "storefrontTelephone": "",
            "businessType": "14",
            "bookContent": "",
            "idBookingSurvey": id_booking_survey,
            "detailaddress": "北京市朝阳区世纪财富中心2号楼2层平安门店",
            "deptCode": "201",
            "contactName": contactName,
            "contactTelephone": contactTelephone,
            "applicantName": "",
            "applicantIdCard": "",
            "bookingSource": "miniApps",
            "businessKey": None,
            "agentFlag": "0",
            "newCarFlag": "0",
            "noPolicyFlag": "0",
            "vehicleNo": vehicleNo,
            "inputPolicyNo": "",
            "latitude": "",
            "longitude": "",
            "offlineItemList": []
        }
        # header
        book_headers = {
            "Content-Type": "application/json",
            "sessionId": Callback.sessionId,
            "signature": Callback.signature
        }
        res = requests.post(booking_url, headers=book_headers, json=body)
        print(res.text)
        if 'success' in res.text:
            print('预约成功')
            input('按回车键结束程序')
            exit()

    def Http(SunnyContext, requestId, MessageId, messageType, requestType, requestUrl, errMessage, pid):
        SyHTTP = SyNet.MessageIdToSunny(MessageId)
        if messageType == Callback.Http_message_request_start:
            SyHTTP.request.del_gzip_tag()
            if b"newretail.pingan.com.cn" in requestUrl:
                Callback.sessionId = SyHTTP.request.get_header_single("sessionId")
                Callback.signature = SyHTTP.request.get_header_single("signature")
                if Callback.sessionId != "" and Callback.signature != "":
                    print("获取成功 sessionId=" + Callback.sessionId + " signature=" + Callback.signature)
                    print("开始测试是否有效(返回-10004和-1501即为正常)")
                    Callback.booking("2023年06月25日 星期日", "10:00", "11:00", "FE8C62EA019420BDE0533106A8C00423")
                    input('按回车键开始预约')
                    Sunny.stop_proxy()
                    while True:
                        try:
                            res = requests.get(Callback.url, headers=Callback.headers, timeout=3)
                            json_data = json.loads(res.text)
                            print('----------------------------------------------------')
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            for data in json_data['data']:
                                if data['totalBookableNum'] > 0:
                                    print('有号')
                                    print(data['bookingDate'])
                                    for i in data['bookingRules']:
                                        if i['bookableNum'] > 0:
                                            print(i['startTime'], '-', i['endTime'], '剩余号数：', i['bookableNum'])
                                            Callback.booking(data['bookingDate'], i['startTime'], i['endTime'],
                                                    i['idBookingSurvey'])
                                else:
                                    print('无号')
                            print('----------------------------------------------------')
                        except Exception as error:
                            print("An exception occurred:", error)
                            print('网络异常')
                            print('----------------------------------------------------')
            pass
        elif messageType == Callback.Http_message_request_fail:
            err = BytesToStr(errMessage)
            print(BytesToStr(requestUrl) + " : 请求错误 :" + err)
            pass
        else:
            pass


contactName = ''
vehicleNo = ''
contactTelephone = ''
Sunny = SyNet.SunnyNet()
Sunny.bind_port(2023)
Sunny.install_cert()
Sunny.bind_callback(Callback.Http, None, None, None)
print("--------------------")
print("平安摩托车投保预约 交流企鹅群：744382753")
print("本程序仅供学习交流，请勿用于非法用途，否则后果自负")
print("本程序免费开源，禁止任何人用于商业用途")
print("--------------------")
if not Sunny.start():
    print("启动失败")
    print(Sunny.get_error_msg())
    exit(0)
else:
    print("正在启动服务...")
    if not Sunny.process_proxy_load_driver():
        print("加载驱动失败，进程代理不可用(注意，需要管理员权限（请检查），win7请安装 KB3033929 补丁)")
    else:
        print("服务启动成功")
        print("请输入手机号")
        contactTelephone = input()
        print("请输入车牌号(格式：京A-A1234或京B-A1234)")
        vehicleNo = input()
        print("请输入姓名")
        contactName = input()
        print("--------------------")
        print("您输入的信息如下：")
        print("手机号：" + contactTelephone)
        print("车牌号：" + vehicleNo)
        print("姓名：" + contactName)
        print("--------------------")
        Sunny.process_proxy_add_process("WeChatAppEx.exe")
        print("请打开PC微信平安产险门店小程序自动获取sessionId和signature")

while True:
    time.sleep(1)
