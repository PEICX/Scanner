# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/29 15:01'

import string

from web_lib.http.URL import URL
from simhash import Simhash
from random import choice, randint


def rand_letters(length=randint(6, 10)):

    t_list = []
    for i in range(length):
        t_list.append(choice(string.ascii_letters))
    return ''.join(t_list)


# URL去除相似和包含
def is_contain_list(lista, listb):
    # 参数是否相似或包含
    if not isinstance(lista, list) or not isinstance(listb, list):
        return False

    if len(lista) >= len(listb):
        temp = lista
        lista = listb
        listb = temp
    count1 = 0
    for item in lista:
        if item in listb:
            count1 += 1

    if count1 == len(lista) and count1 <= len(listb):
        return True
    return False


def is_similar_url(urla, urlb):
    # 判断url是否相似和包含
    if not isinstance(urla,URL):
        urla = URL(urla)

    if not isinstance(urlb,URL):
        urlb = URL(urlb)

    url1_str = urla.url_string
    url2_str = urlb.url_string

    qs1 = urla.get_query().keys()
    qs2 = urlb.get_query().keys()

    if url1_str == url2_str and is_contain_list(qs1, qs2):
        return True
    return False


def is_similar_page(res1, res2, radio=3):
    # 使用simHash判断页面的相似程度
    if res1 is None or res2 is None:
        return False

    body1 = res1.body
    body2 = res2.body

    # 此处非常耗时，大概是split函数费时
    simhash1 = Simhash(body1.split())
    simhash2 = Simhash(body2.split())

    calc_radio = simhash1.distance(simhash2)

    if calc_radio <= radio:
        return True
    return False


if __name__ == "__main__":
    print(rand_letters(8))