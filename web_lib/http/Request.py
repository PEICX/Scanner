#coding=utf-8
'''
Request.py
'''

import copy
import uuid

from web_lib.http.URL import URL
from web_lib.utils.UserAgent import get_useragent


class Request(object):
    '''
    传入一个URL对象，默认是GET方法，对他进行进一步封装，便于cur类的send_req方法直接使用进行请求
    '''
    DEFAULT_USER_AGENT = get_useragent()

    def __init__(self,url,method='GET',headers=None,cookies=None,referer=None,data=None,user_agent=DEFAULT_USER_AGENT,**kwargs):
        '''
        '''
        if isinstance(url,URL):
            self._url = url
        else:
            self._url = URL(url)

        self._method = method
        # uuid是干嘛的？唯一标识一个对象
        self.id = uuid.uuid1()

        self._headers = {}
        if headers:
            self._headers.update(headers)

        self._cookies  = cookies

        self._referer = referer

        self._user_agent = user_agent
        # 在headers中直接传cookie方便，使用cookie参数变量传输，需保证cookie是一个dict，格式化麻烦还容易出错
        if self._cookies:
            self._headers.update({"Cookie": self._cookies})

        if self._referer:
            self._headers.update({"Referer": self._referer})

        if self._user_agent:
            self._headers.update({"User-Agent": self._user_agent})

        
        self._get_data  = self._url.get_query()

        self._post_data = data if data else ""

    def get_get_param(self):
        return self._get_data

    def get_post_param(self):
        return self._post_data

    def get_url(self):
        return self._url

    def get_method(self):
        return self._method

    def get_id(self):
        return self.id

    def get_headers(self):
        return self._headers

    def get_cookies(self):
        return self._cookies

    def set_method(self,method):
        self._method = method.upper()

    def set_post_data(self,postdata):
        self._post_data = postdata

    def set_get_data(self,getdata):
        self._get_data  = getdata

    def set_referer(self,referer):
        self._referer = referer

    def set_cookies(self,cookies):
        self._cookies = cookies

    def __eq__(self, other):
        if self._url == other._url and self._method == other._method:
            return True
        else:
            return False

    def __str__(self):
        result_string = self._method

        result_string +=" "+self._url.url_string + " HTTP/1.1\r\n"

        headers = copy.deepcopy(self._headers)
        headers.update({"Host":self._url.get_host()})

        for key,value in headers.items():
            result_string +=key+": "+value
            result_string +="\r\n"

        result_string +="\r\n"

        if self._method=="POST":
            result_string +=str(self._post_data)

        return result_string

    def __repr__(self):
        vals = {'method':self.get_method(),'url':self.get_url().url_string,'id':self.get_id()}

        return '<Request | %(method)s | %(url)s | %(id)s>' % vals

if __name__=="__main__":
    req = Request("http://www.baidu.com/index.php?id=1")
    print(req.get_get_param())
    print(req.get_url())
    print(req)
    
    a = []
    a.append(req)
    print(a)
