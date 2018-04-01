# _*_ coding: utf-8 _*_


from http.client import HTTPConnection

import requests
import socket

from settings import COOKIES, PROXIES, DEBUGSWITCH
from web_lib.http.Response import Response, from_requests_response
from web_lib.http.URL import URL
from web_lib.utils.UserAgent import get_useragent

'''
对requests库结合自定义的Request和Response类进一步封装
'''

socket.setdefaulttimeout(60)

class Durl:

    def __init__(self):

        self._time = 0.0
        self._speed = 20
        self._conn = 0

        self._scan_signature = get_useragent()
        self._scan_proxies = PROXIES

        HTTPConnection.debuglevel = DEBUGSWITCH

    def get_default_headers(self, headers):
        default_headers = {"User-Agent": self._scan_signature}
        default_headers.update(headers)
        return default_headers


    def get(self, url, headers={}, **kwargs):
        default_headers = self.get_default_headers(headers)

        if not isinstance(url, URL):
            url = URL(url)

        requests_response = None
        try:
            requests_response = requests.get(url.url_string, headers=default_headers, **kwargs)

        except Exception as e:
            print(e)
            return self._make_response(requests_response, url)

        response = self._make_response(requests_response, url)

        return response


    def post(self, url, headers={}, data=None, **kwargs):
        default_headers = self.get_default_headers(headers=headers)
        if not isinstance(url, URL):
            url = URL(url)

        requests_response = None
        try:
            requests_response = requests.post(url.url_string, headers=default_headers, data=data, **kwargs)
        except:
            return self._make_response(requests_response, url)
        response = self._make_response(requests_response, url)
        return response


    def _make_response(self, resp_from_requests, req_url):
        '''
        把请求的结果储存在Response类中；
        '''
        if resp_from_requests is None:
            response = Response(req_url=req_url)
        else:
            response = from_requests_response(resp_from_requests, req_url)

        return response

    def send_req(self, req):
        '''
        传入Request类，来执行新的请求；
        '''
        method = req.get_method()
        uri = req.get_url().url_string
        querystring = req.get_get_param()
        postdata = req.get_post_param()
        headers = req.get_headers()
        if COOKIES == True:
            cookies = req.get_cookies()
        else:
            cookies = ""
        proxies = self._scan_proxies
        send = getattr(requests, method.lower())
        requests_response = None
        try:
            requests_response = send(uri, params=querystring, data=postdata, headers=headers, cookies=cookies,proxies=proxies)

        except Exception as e:
            print(e)
            return self._make_response(requests_response, req.get_url())
        else:
            response = self._make_response(requests_response, req.get_url())
            return response

curl = Durl()

if __name__ == "__main__":
    from web_lib.http.Request import Request
    req = Request(url="http://127.0.0.1:8000/form/")
    a =curl.send_req(req)

    pass