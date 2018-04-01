#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-25 11:22:09
# @Author  : Law Paul (peicx@outlook.com)
# @Link    : http://github.com/peicx
# @Version : $Id$

from celery_app import scan_task

scan_task.DoScanTask.delay()        # 也可用 task1.add.delay(2, 8)
  # 也可用 task2.multiply.delay(3, 7)

print('hello world')
