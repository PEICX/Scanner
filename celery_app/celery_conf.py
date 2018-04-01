#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-25 11:18:32
# @Author  : Law Paul (peicx@outlook.com)
# @Link    : http://github.com/peicx
# @Version : $Id$


# broker是任务调度队列，接收任务生产者发来的消息（即任务），将任务存入队列；
# celery本身不提供这个，这里用Redis实现；
BROKER_URL = 'redis://127.0.0.1:6379'
# Backend 用于存储任务的执行结果，以供查询。同消息中间件一样，这里使用Redis；
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC

CELERY_IMPORTS = (                                  # 指定导入的任务模块
    'celery_app.scan_task'
)

# 限制任务速率
# CELERY_ANNOTATIONS = {
#     'tasks.add': {'rate_limit': '10/m'}
# }
