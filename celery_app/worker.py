# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/31 16:53'

from celery_app import app


if __name__=="__main__":
	app.worker_main()