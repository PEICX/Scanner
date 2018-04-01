# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/31 17:24'


version="1.0"

banner='''
  ____    
 / ___|  ___ __ _ _ __  _ __   ___ _ __ 
 \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|\033[1;31m{%s}\033[0m
  ___) | (_| (_| | | | | | | |  __/ |   
 |____/ \___\__,_|_| |_|_| |_|\___|_|   
'''% (version)


def scan_banner():
    print(banner)

if __name__ == "__main__":
    scan_banner()
