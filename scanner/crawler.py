# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/29 22:14'

'''
网站前的协议就不要加了，如https，会显示ssl错误，有空在修改这个吧
'''
import time, itertools
from queue import Queue

from utils.LogManager import log
from web_lib.utils.common import is_similar_url
from web_lib.http.Request import Request
from web_lib.http.URL import URL
from web_lib.utils.page_404 import is_404
from web_lib.http.downloadUrl import curl
from web_lib.parser.dpCache import dpc
from web_lib.utils.url_filter import Filter


class Crawler(object):
    def __init__(self, depth_limit=1, time_limit=30, req_limit=100, filter_similar=True):

        self.root = ''

        self._target_domain = ''

        self.depth_limit = depth_limit
        self.time_limit = time_limit
        self.req_limit = req_limit

        self._sleeptime = 1

        self._url_list = []

        self.seen = Filter()

        self._relate_ext = ['html', 'shtm', 'htm', 'shtml']

        self._white_ext = ['asp', 'aspx', 'jsp', 'php', 'do', 'action']

        self._black_ext = ["ico", "jpg", "gif", "js", "png", "bmp", "css", "zip", "rar", "ttf"]

        self._blockwords = ['mailto:', 'javascript:', 'file://', 'tel:']

        self.num_urls = 0

        self.num_reqs = 0
        # 保存所有爬到的url
        self._wRequestList = []

        self._start_time = None

        self._other_domains = set()

    def get_discovery_time(self):
        '''
        爬虫爬行的时间，单位为：分钟
        '''
        now = time.time()
        diff = now - self._start_time

        return diff / 60

    def _do_with_reqs(self, reqs):
        '''
        过滤相似和包含的请求
        传入一个内容是url的list（列表内已去重），返回过滤相似和包含后的url list
        '''
        result = []
        try:
            count = len(reqs)
        except Exception:
            print("crawler, line75, object of type 'NoneType' has no len()")
            return result
        if count == 0:
            return result

        for i in range(count):
            filter = False
            filter_url = reqs[i].get_url()
            for j in range(count - i - 1):
                k = i + j + 1
                store_url = reqs[k].get_url()
                if is_similar_url(filter_url, store_url):
                    filter = True
                    break
            if not filter:
                result.append(reqs[i])

        return result

    def _get_reqs_from_resp(self, response):
        '''
        :param response: 输入的参数是curl请求返回的Response类；
        使用HtmlParser方法提取响应中所有的url
        :return: 返回一个包含url的list
        '''
        new_reqs = [] # 临时保存本次解析响应正文得到的url
        try:
            doc_parser = dpc.getDocumentParserFor(response)
        except Exception as e:
            pass
        else:
            re_urls, tag_urls = doc_parser.get_get_urls()
            form_reqs = doc_parser.get_form_reqs()
            seen = set()
            for new_url in itertools.chain(re_urls, tag_urls):
                if new_url in seen:
                    continue
                seen.add(new_url)
                if new_url.get_host() != self._target_domain:
                    if new_url.get_host() not in self._other_domains:
                        self._other_domains.add(new_url.get_host())
                    continue
                if new_url not in self._url_list:
                    self._url_list.append(new_url)
                    wreq = self._url_to_req(new_url, response)
                    if wreq not in self._wRequestList:
                        new_reqs.append(wreq)
                        self._wRequestList.append(wreq)

            for item in form_reqs:
                if item not in self._wRequestList:
                    new_reqs.append(item)
                    self._wRequestList.append(item)
            return new_reqs

    def _url_to_req(self, new_url, response, method="GET"):
        '''
        输入url，返回一个Request类，便于直接请求；
        同时根据传入的response设置请求的referer和cookies
        '''
        req = Request(new_url)
        req.set_method(method)

        new_referer = response.get_url()
        req.set_referer(new_referer)

        new_cookies = response.get_cookies()
        req.set_cookies(new_cookies)

        return req

    def crawl(self, root_url):
        '''
        将URL对象存入到队列
        '''
        if not isinstance(root_url, URL):
            root_url_obj = URL(root_url)
        else:
            root_url_obj = root_url

        self._target_domain = root_url_obj.get_host()

        self._url_list.append(root_url_obj)

        root_req = Request(root_url_obj)

        q = Queue()

        q.put((root_req, 0))

        self._start_time = time.time()

        while True:

            if q.empty():
                print("reqs empty break")
                break

            this_req, depth = q.get()

            # 将静态链接进行过滤
            if this_req.get_url().get_ext() in self._black_ext:
                continue

            # 控制爬行的深度
            if depth > self.depth_limit:
                print("depth limit break")
                break
            # 控制爬行的时间
            if self.get_discovery_time() > self.time_limit:
                print("time limit break")
                break

            # 控制爬行的链接数，避免内存泄露
            if self.num_reqs > self.req_limit:
                print("reqs num limit break")
                break

            # 此处url去重，未访问过会自动加入set中
            if self.seen.request_seen(this_req):
                continue

            log.info("%s Request:%s" % (this_req.get_method(), this_req.get_url().url_string))

            response = None

            try:
                response = curl.send_req(this_req)
            except Exception as e:
                print(str(e))
                pass

            if is_404(response):
                continue

            if response is None:
                continue
            # 获取HTTP响应中的请求
            new_reqs = self._get_reqs_from_resp(response)
            # 过滤相似和包含的请求
            filter_reqs = self._do_with_reqs(new_reqs)

            depth = depth + 1
            for req in filter_reqs:
                q.put((req, depth))

            self.num_reqs = self.seen.get_len()
            log.info("Already Send Reqs:" + str(self.num_reqs) + " Left Reqs:" + str(q.qsize()))

            time.sleep(self._sleeptime)

        return self._do_with_reqs(self._wRequestList)
