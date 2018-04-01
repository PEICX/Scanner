#
# import logging
# logging.basicConfig(level=logging.INFO)
# from scanner.crawler import Crawler
#
# if __name__=="__main__":
#     # scan_task.DoScanTask.delay("1")
#     logging.info("Scanner Get the Msg From the Task Queue")
#     spider = Crawler().crawl("http://127.0.0.1:8000/form/")
#     for i in spider:
#         print(i.get_url())
#
#


class A():
    def __init__(self):

        self.a = 1
        self.b = 2
    def h(self):

        print(self['a'])
    def __setattr__(self, key, value):
        self.__dict__[key] = value
    def __getattr__(self, key):
        return self.__dict__[key]


a = A()
a.h()