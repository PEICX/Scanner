# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/18 19:19'

'''
对URL类进行封装，URL的多元信息，比如，主机名，端口，根域名，文件名，
扩展名和请求参数等，方便操作和处理
'''

from urllib.parse import urlparse, urlunparse, urljoin, parse_qs


class URL:

    def __init__(self, url):

        # startswith字符串的方法，检查字符串的开头是否符合要求
        if not url.startswith("https://") and not url.startswith("http://"):
            url = "http://" + url
        urlres = urlparse(url)
        self.scheme = urlres.scheme # 协议
        self.port = 80 if urlres.port is None else urlres.port
        self.netloc = urlres.netloc if urlres.netloc.find(':')>-1 else urlres.netloc+':'+str(self.port)
        self.path = urlres.path
        self.params = urlres.params
        self.qs = urlres.query
        self.fragment = urlres.fragment

    def get_domain(self):
        return self.netloc.split(":")[0]

    def get_host(self):
        # 获取主机名
        return self.netloc.split(":")[0]

    def get_port(self):
        return self.port

    def get_path(self):
        return self.path

    def get_filename(self):
        # 获取URL中的文件名
        return self.path[self.path.rfind('/')+1:]

    def get_ext(self):
        # URL中文件扩展名
        fname = self.get_filename()
        ext = fname[fname.rfind('.')+1:]
        return '' if ext == fname else ext

    def get_query(self):
        return parse_qs(self.qs)

    def urljoin(self, relative):

        jurl = urljoin(self.url_string, relative)
        jurl_obj = URL(jurl)

        return jurl_obj

    @property
    def url_string(self):

        data = (self.scheme, self.netloc, self.path, self.params, self.qs, self.fragment)
        return urlunparse(data)


    def __str__(self):
        return "%s" %(self.url_string)

    def __repr__(self):
        return '&lt;URL for "%s"&gt;' % (self.url_string)


if __name__ == '__main__':
    url = "www.baidu.com/l;jkf/dfasd;f/in?a=1&b=2#lkafjds"
    a = URL(url)
    b = a.url_string
    c = a.get_path()
    d = a.get_domain()
    q = a.qs
    pass