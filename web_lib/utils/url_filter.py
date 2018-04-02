# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/4/2 21:00'

import hashlib


class Filter():
    def __init__(self):
        self._fingerprints = set()

    def request_seen(self, request):
        fp = self._request_fingerprint(request)
        if fp in self._fingerprints:
            return True
        self._fingerprints.add(fp)
        return False


    def _request_fingerprint(self, request):

        fp = hashlib.sha1()
        fp.update(request.get_method().encode())
        fp.update(request.get_url().url_string.strip('/').encode())
        # 生成40位长度的字符串
        return fp.hexdigest()

    def get_len(self):
        return len(self._fingerprints)





if __name__=="__main__":
    from web_lib.http.Request import Request

    seen = Filter()
    print(seen.request_seen(Request(url='www.baidu.com')))
    print(seen.get_len())
    print(seen.request_seen(Request(url='www.baidu.com/')))
    print(seen.get_len())
    print(seen.request_seen(Request(url='http://www.baidu.com//')))
    print(seen.get_len())
    print(seen.request_seen(Request(url='https://www.baidu.com')))
    print(seen.get_len())
    print(seen.request_seen(Request(url='www.baidu.com/1')))
    print(seen.get_len())