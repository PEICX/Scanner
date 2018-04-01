# _*_ coding: utf-8 _*_
import apply as apply

__author__ = 'PEICX'
__date__ = '2018/3/27 19:27'

from fake_useragent import UserAgent
from settings import USER_AGENT



def random_user_agent():
        return UserAgent().random



def get_useragent():
        if USER_AGENT == "random_user_agent":
            return random_user_agent()
        else:
            return "PScanner/1.0"