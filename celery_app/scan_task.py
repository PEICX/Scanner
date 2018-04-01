# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/31 16:25'


from utils.LogManager import log as logging
from celery_app import app
from time import sleep

@app.task(ignore_result=True)
def DoScanTask(msg_info):
    logging.info("Scanner Get the Msg From the Task Queue")
    for i in range(100):
        print(i)
        sleep(5)
    print("closed.................")





