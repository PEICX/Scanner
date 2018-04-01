# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/28 10:04'

import re, urllib, traceback

from utils.LogManager import log as logging
from settings import DEFAULT_ENCODING
from web_lib.http.URL import URL
from lxml import etree
from web_lib.http.Request import Request
from web_lib.utils.smart_fill import smart_fill
from web_lib.http.Data import postData

class HtmlParser():


    URL_HEADERS = ('location')
    URL_TAGS = (
    'a', 'img', 'link', 'script', 'iframe', 'object', 'embed', 'area', 'frame', 'applet', 'input', 'base', 'div',
    'layer', 'form')
    URL_ATTRS = ('href', 'src', 'data', 'action')
    URL_RE = re.compile('((http|https)://([\w:@\-\./]*?)[^ \n\r\t"\'<>)\s]*)')
    SAFE_CHARS = (('\x00', '%00'),)

    def __init__(self, response):
        # set variables
        self._encoding = DEFAULT_ENCODING
        self._base_url = response.get_url()
        self._cookie = response.get_cookies()

        # Internal state variables
        self._inside_form = False
        self._inside_select = False
        self._inside_textarea = False
        self._inside_script = False

        # Internal containers
        self._tag_and_url = set()
        self._parsed_urls = set()

        self._g_urls = set()
        self._p_urls = set()

        self._forms = []
        self._comments_in_doc = []
        self._scripts_in_doc = []
        self._meta_redirs = []
        self._meta_tags = []

        # To store results
        self._emails = []
        self._form_reqs = []
        self._re_urls = set()
        self._tag_urls = set()

        # Do some stuff before actually parsing
        self._pre_parse(response)

        # Parse!
        self._parse(response)

    def _pre_parse(self, response):
        # 提取Header里的URL
        dict_headers = response.headers
        str_headers = ""

        for key, val in dict_headers.items():
            str_headers += key + ":" + val + "\r\n"

        self._regex_url_parse(str_headers)
        self._find_header_urls(dict_headers)
        self._regex_url_parse(response.body)

    def _parse(self, response):
        # lxml提取
        parser = etree.HTMLParser(target=self, recover=True)
        try:
            # 根据标签内容自动调用start和end函数；
            etree.fromstring(response.body, parser)
        except ValueError:
            pass

    # 获取响应头中的URL
    def _find_header_urls(self, headers):

        for key,value in headers.items():
            if key in self.URL_HEADERS:
                if value.startswith("http"):
                    url = URL(value)
                else:
                    url = self._base_url.urljoin(value).url_string
                    url = URL(url)
                print(url)
                self._tag_urls.add(url)

    # 获取满足URL形式的数据
    def _regex_url_parse(self, doc_str):

        re_urls = set()

        for url in re.findall(HtmlParser.URL_RE, doc_str):
            try:
                url = URL(url[0])
            except ValueError:
                pass
            else:
                re_urls.add(url)

        def find_relative(doc_str):
            res = set()
            # 形如index.php或index.php?aid=1&bid=2的相对URL
            regex = '([/]{0,1}\w+\.(asp|html|php|jsp|aspx|htm)(\?([\w%]*=[\w%]*)(&([\w%]*=[\w%]*))*){0,1})'
            relative_regex = re.compile(regex, re.U | re.I)
            for match_tuple in relative_regex.findall(doc_str):
                match_str = match_tuple[0]
                url = self._base_url.urljoin(match_str).url_string
                url = URL(url)
                res.add(url)
            return res

        re_urls.update(find_relative(doc_str))
        self._re_urls.update(re_urls)


    def start(self, tag, attrs):
        # 遇到tag的开始，如<a>，parser自动调用该函数，start结尾的函数负责逐个标签收集数据
        # 比如表单标签，没遇到结束标签前都要处理，防止漏掉
        try:
            # 根据标签调用对应的处理函数
            meth = getattr(self, '_handle_' + tag + '_tag_start', lambda *args: None)

            meth(tag, attrs)

            if tag.lower() in self.URL_TAGS:
                self._find_tag_urls(tag, attrs)

        except Exception as ex:
            msg = 'An exception occurred while parsing a document: %s' % ex
            logging.error(msg)
            logging.error('Error traceback: %s' % traceback.format_exc())


    def end(self, tag):
        # 遇到闭合标签，如</a>,parser自动调用end函数，end结尾的函数负责收集完数据后，把数据进行处理，方便request直接请求
        # 比如表单，end使用start收集好的信息，然后处理化为一个Request对象，方便后续使用；
        getattr(self, '_handle_' + tag + '_tag_end', lambda arg: None)(tag)

    def close(self):
        pass

    # 获取内容标签中的URL
    def _find_tag_urls(self, tag, attrs):

        for attr_name, attr_value in attrs.items():
            if attr_name in self.URL_ATTRS and attr_value and not attr_value.startswith("#"):
                try:
                    if attr_value.startswith("http"):
                        url = URL(attr_value)
                    else:
                        url = self._base_url.urljoin(attr_value).url_string
                        url = URL(url)
                except ValueError:
                    pass
                else:
                    self._tag_urls.add(url)

    @property
    def forms(self):
        return self._forms

    def get_forms(self):
        return self.forms

    @property
    def urls(self):
        return self._re_urls,self._tag_urls

    def get_get_urls(self):
        return self._re_urls,self._tag_urls

    def get_form_reqs(self):
        return self._form_reqs


    def _handle_form_tag_start(self, tag, attrs):
        self._inside_form = True
        method = attrs.get('method', 'POST')
        name = attrs.get('name', '')
        action = attrs.get('action', None)

        missing_or_invalid_action = action is None

        if not missing_or_invalid_action:
            try:
                action = self._base_url.urljoin(action)
            except ValueError:
                missing_or_invalid_action = True

        if missing_or_invalid_action:
            action = self._base_url

        form_data = postData()
        form_data.set_name(name)
        form_data.set_method(method)
        form_data.set_action(action)

        self._forms.append(form_data)

    def _handle_form_tag_end(self, tag):

        self._inside_form = False

        form_data = self._forms[-1]
        url = form_data.get_action()
        method = form_data.get_method()

        freq = Request(url)
        freq.set_method(method)
        freq.set_post_data(form_data)
        # enable cookie，有时候要禁止这个
        freq.set_cookies(self._cookie)

        self._form_reqs.append(freq)

    def _handle_input_tag_start(self, tag, attrs):

        side = 'inside' if self._inside_form else 'outside'
        # 为什么这么做，我也不知道
        default = lambda *args: None
        meth = getattr(self, '_handle_' + tag + '_tag_' + side + '_form', default)
        meth(tag, attrs)


    def _handle_input_tag_inside_form(self, tag, attrs):

        form_data = self._forms[-1]

        type = attrs.get('type', '').lower()
        name = attrs.get('name', '')
        value = attrs.get('value', '')
        items = attrs.items()

        if name == '':
            return

        if value == "":
            value = smart_fill(name)

        if type == 'file':
            form_data.hasFileInput = True
        else:
            form_data.set_data(name, value)


if __name__ == '__main__':
    from web_lib.http.downloadUrl import curl
    res = curl.get(url="http://127.0.0.1:8000/form/", allow_redirects=True)
    a = HtmlParser(res)
    b = a.urls
    c = curl.send_req(a.get_form_reqs()[-1])
    pass