# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @Site    : 平安预约号
# @Software: PyCharm
import threading

import requests
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
}

# 日期时间戳
timestamp = int(time.time() * 1000)
sessionId = '********'
signature = '*******'
contactName = '*****'
vehicleNo = '京B-*****'
contactTelephone = '*******'

# 预约接口
url = 'https://newretail.pingan.com.cn/ydt/reserve/store/bookingTime?storefrontseq=39807&businessType=14&time={}'.format(
    timestamp)


# 开始预约 参数1 预约时间 参数2 预约时间段
def booking(date, start_time, end_time, id_booking_survey):
    # 预约接口
    booking_url = 'https://newretail.pingan.com.cn/ydt/reserve/reserveOffline?time={}'.format(timestamp)
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
        "sessionId": sessionId,
        "signature": signature
    }
    res = requests.post(booking_url, headers=book_headers, json=body)
    print(res.text)
    if 'success' in res.text:
        print('预约成功')
        input('按回车键结束程序')
        exit()
        # 如果返回-10004则继续预约
    elif '10004' in res.text:
        booking(date, start_time, end_time, id_booking_survey)


# 测试
print('测试预约')
booking("2023年06月25日 星期日", "10:00", "11:00", "FE8C62EA019420BDE0533106A8C00423")
input('按回车键开始预约')
while True:
    try:
        res = requests.get(url, headers=headers, timeout=3)
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
                        t = threading.Thread(target=booking, args=(data['bookingDate'], i['startTime'], i['endTime'], i['idBookingSurvey']))
                        t.start()
            else:
                print('无号')
        print('----------------------------------------------------')
    except Exception as error:
        print("An exception occurred:", error)
        print('网络异常')
        print('----------------------------------------------------')
