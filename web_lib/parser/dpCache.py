# _*_ coding: utf-8 _*_


__author__ = 'PEICX'
__date__ = '2018/3/31 15:51'

import threading

from web_lib.parser.documentParser import documentParser
from web_lib.parser.lru import LRU


class dpCache:
    '''
    缓存池，缓存30个，解析之前，取body的hash，先看看缓存中有没有
    '''
    def __init__(self):
        self._cache = LRU(30)
        self._LRULock = threading.RLock()

    def getDocumentParserFor(self, Response):

        res = None
        hash_string = hash(Response.body)

        with self._LRULock:
            if hash_string in self._cache:
                res = self._cache[hash_string]
            else:
                # Create a new instance of dp, add it to the cache
                res = documentParser(Response)
                self._cache[hash_string] = res

            return res


dpc = dpCache()
