# _*_ coding: utf-8 _*_


from http.client import HTTPConnection

import requests
import socket

from settings import COOKIES, PROXIES, DEBUGSWITCH
from web_lib.http.Response import Response, from_requests_response
from web_lib.http.URL import URL
from web_lib.utils.UserAgent import get_useragent


socket.setdefaulttimeout(60)

class Durl:
    '''
    输入：对原始request类进行封装，使其get和post方法支持直接使用URL类；
         同时支持直接使用Request类进行请求（send_req方法）；
    输出：请求结果返回值为封装为自定义的Respone类；

    '''

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
        输入是原始request请求返回的结果；
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
        # 此处的headers包括了自动跟踪的cookie了
        headers = req.get_headers()
        proxies = self._scan_proxies
        requests_response = None
        if method == 'GET':
            requests_response = requests.get(uri, params=querystring, headers=headers,
                                     proxies=proxies)
        elif method == 'POST':
            requests_response = requests.post(uri, params=querystring, data=postdata, headers=headers, proxies=proxies)

        response = self._make_response(requests_response, req.get_url())
        return response

curl = Durl()

if __name__ == "__main__":
    from web_lib.http.Request import Request
    req = Request(url="www.baidu.com")
    a =curl.send_req(req)

    pass