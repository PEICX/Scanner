# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/29 15:28'

from urllib.parse import urljoin

from web_lib.utils.common import is_similar_page, rand_letters
from web_lib.http.downloadUrl import curl


class page_404:

    _instance = None

    def __init__(self):
        self._404_already_domain = []
        self._404_kb = []
        self._404_code_list = [200, 301, 302]

    def generate_404_kb(self, url):

        domain = url.get_domain()
        domain_path = domain + url.get_path()
        if '/' not in domain_path:
            domain_path = domain_path + '/'
        rand_file = rand_letters(8) + '.html'
        url_404 = urljoin(domain_path, rand_file)
        resp_200 = curl.get(domain_path)
        resp_404 = curl.get(url_404)

        if not is_similar_page(resp_200, resp_404):
            # 404页面与正常页面相同
            pass
        else:
            self._404_already_domain.append(domain)
            self._404_kb.append((domain, resp_404))

    def is_404(self, http_response):

        code = http_response.get_code()
        url = http_response.get_url()
        domain = url.get_domain()
        if domain not in self._404_already_domain:
            self.generate_404_kb(url)

        if code == 404:
            return True

        if code in self._404_code_list:
            for domain_404, resp_404 in self._404_kb:
                if domain == domain_404:
                    if is_similar_page(http_response, resp_404):
                        return True
        return False

    def set_check(self):
        self._404_kb = []
        self._404_checked = False


def is_404(http_response):
    if page_404._instance is None:
        page_404._instance = page_404()
    return page_404._instance.is_404(http_response)


if __name__ == "__main__":
    url = "http://www.baidu.com/"
    res = curl.get(url)

    if is_404(res):
        print("404")
