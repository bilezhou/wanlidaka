# -*- coding:utf-8 -*-
import re
import requests
import json

'''--------只填这里----------'''
xuehao = '202xxxxxxx'#这里填学号
mima = 'xxxxxxxxx'#这里填密码
'''-------------------------'''
tagid='0ee8ce1900494a42a8d0502cdbdf4b81'
#问卷ID 2月3日起：0ee8ce1900494a42a8d0502cdbdf4b81
#历史1：26e499d23ff64acbb2db0b504f6f36b6

def all():
    cookies = getcookie()
    if len(cookies) > 0:
        da = postinfo(cookies)
        postpickcard(da, cookies)
    else:
        print(xuehao + "账号密码不正确！")

def getcookie():
    url = "https://ehallapp.zwu.edu.cn:8080/_layouts/15/ZWUWSBS/AppApi/System/AuthApi.aspx"
    payload = "{\"PostBackType\":\"LoginApp\",\"Data\":{\"Account\":\"" + xuehao + "\",\"Password\":\"" + mima + "\",\"AppVersion\":\"2.13\"},\"IsAppRequest\":true}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'Origin': 'https://ehallapp.zwu.edu.cn:8080',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'Set-Cookie' in response.headers:
        setcookies = response.headers['Set-Cookie']
        G2UserToken = re.match(r'G2UserToken.*?;', setcookies)
        ZWU = re.findall(r'ZWU.*?;', setcookies)
        cookies = str(G2UserToken[0]) + 'loginstatus=1;' + str(ZWU[0])  # 组装cookie
    else:
        cookies = ''
    return cookies
def postinfo(coo):
    cookies = coo
    url = "https://ehallapp.zwu.edu.cn:8080/_layouts/15/ZWUWSBS/AppApi/HealthReport/InformationReportApi.aspx"
    payload = "{\"PostBackType\":\"getUserViewData\",\"Id\":\""+tagid+"\",\"IsAppRequest\":true}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'Origin': 'https://ehallapp.zwu.edu.cn:8080',
        'Cookie': cookies,
        'Content-Type': 'application/json'
    }
    data = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
    data.pop("ElapsedTime")
    data.pop("RetFlag")
    data.pop("RetCode")
    data.pop("Message")
    data["RequestObject"] = data.pop("Data")
    data["PostBackType"] = "saveUserViewData"
    data = json.loads(json.dumps(data))
    data["IsAppRequest"] = True
    data['RequestObject']['SortAscending'] = False
    payload = json.dumps(data)
    return payload
def postpickcard(da, cook):
    payload = da
    cookies = cook
    url = "https://ehallapp.zwu.edu.cn:8080/_layouts/15/ZWUWSBS/AppApi/HealthReport/InformationReportApi.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'Origin': 'https://ehallapp.zwu.edu.cn:8080',
        'Cookie': cookies,
        'Content-Type': 'application/json'
    }
    res = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    data = json.loads(res.text)
    if data['RetCode'] == 0:
        print('恭喜您！' + data['Data']['Author'] + '，打卡成功！打卡时间：' + data['Data']['Created'])
    else:
        print('打卡失败！')
        print('data')
print(all())