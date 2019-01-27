#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 0:12
# @Author  : NieLamu
# @Email   : mxmxlty@gmail.com
# @File    : tt.py
# @Description: init


import requests
import webbrowser
import re
from wox import Wox, WoxAPI


QUERY_URL = 'https://m.fanyi.qq.com/translate'
RESULT = {
    'Title': 'Translate between Chinese and English',
    'SubTitle': 'Powered By Tencent Translate, click to open fanyi.qq.com.',
    'JsonRPCAction': {
        'method': 'openUrl',
        'parameters': ['https://fanyi.qq.com']
    },
    'IcoPath': 'img/logo.ico'
}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
}
ZH = re.compile(u'[\u4e00-\u9fa5]+')
PAYLOAD = {
    'from': 1,
    'to': 0,
    'sourceText': '',
    'type': 1,
    'latitude': 1,
    'longitude': 1,
    'platform': 'H5',
}


class Main(Wox):
    def request(self, url):
        # 如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url, proxies=proxies)
        else:
            return requests.get(url)

    # 必须有一个query方法，用户执行查询的时候会自动调用query方法
    def query(self, param):
        results = []
        if param:
            # match = ZH.search(param)
            match = isChinese(param)
            if match:
                PAYLOAD['from'] = 0
                PAYLOAD['to'] = 1
            else:
                PAYLOAD['from'] = 1
                PAYLOAD['to'] = 0
            PAYLOAD['sourceText'] = param
            r = requests.post(QUERY_URL, data=PAYLOAD, headers=HEADERS)
            resp = r.json()
            RESULT
            if resp['targetText']:
                results.append({
                    'Title': resp['targetText'],
                    'SubTitle': resp['source'] + ' to ' + resp['target'],
                    'IcoPath': 'img/logo.ico'
                })
            else:
                results.append({
                    'Title': 'No result. Try another word.',
                    'SubTitle': 'Click here to open the website.',
                    'JsonRPCAction': RESULT['JsonRPCAction'],
                    'IcoPath': 'img/logo.ico'
                })
        else:
            results.append(RESULT)
        return results

    def openUrl(self, url, q=None):
        webbrowser.open(url)
        # WoxAPI.change_query(url)


def isChinese(param):
    if param >= u'\u4e00' and param <= u'\u9fa5':
        return True
    else:
        return False

if __name__ == "__main__":
    Main()