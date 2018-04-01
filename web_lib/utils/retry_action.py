# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/29 21:28'

'''
超时重连的修饰器
requests库默认会进行三次重连尝试
'''

import time
from utils.LogManager import log as logging


def retry_action(retry_num=3):
    def decorator(function):
        cnt = [0]
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                if cnt[0] < retry_num:
                    cnt[0] += 1
                    logging.warning("Retry Connect Count: "+str(cnt[0]))
                    time.sleep(1)
                    return wrapper(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    import requests

    def test():
        requests.get("http://www.testbucunzai.com")

    test()



