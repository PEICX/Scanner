#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-25 11:32:01
# @Author  : Law Paul (peicx@outlook.com)
# @Link    : http://github.com/peicx
# @Version : $Id$

from celery import Celery

app = Celery('scan')                                # 创建 Celery 实例
app.config_from_object('celery_app.celery_conf')   # 通过 Celery 实例加载配置模块
