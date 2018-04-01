# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/25 19:56'

import socket
_dnscache = {}

def _setDNSCache():
    def _getaddrinfo(*args, **kwargs):
        global _dnscache
        if args in _dnscache:
            return _dnscache[args]
        else:
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo



def test():
    from time import sleep
    _setDNSCache()
    import requests
    r1 = requests.get('https://baidu.com')
    print(r1.elapsed.microseconds)
    sleep(3)
    r2 = requests.get('https://baidu.com')
    print(r2.elapsed.microseconds)
    sleep(3)
    r3 = requests.get('https://baidu.com')
    print(r3.elapsed.microseconds)
    sleep(3)
    r4 = requests.get('https://baidu.com')
    print(r4.elapsed.microseconds)
    sleep(3)
    r5 = requests.get('https://baidu.com')
    print(r5.elapsed.microseconds)

