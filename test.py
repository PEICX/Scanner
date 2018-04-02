
import logging
logging.basicConfig(level=logging.INFO)
from scanner.crawler import Crawler

if __name__=="__main__":
    # scan_task.DoScanTask.delay("1")
    logging.info("Scanner Get the Msg From the Task Queue")
    spider = Crawler().crawl("www.baidu.com")
    pass



