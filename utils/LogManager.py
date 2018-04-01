# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/31 17:14'

import logging

logging.basicConfig(format='%(name)s[%(levelname)s/%(process)d]:%(asctime)s:%(module)s.%(funcName)s.%(lineno)d - %(message)s')
log = logging.getLogger("Scanner")
log.setLevel(logging.INFO)
