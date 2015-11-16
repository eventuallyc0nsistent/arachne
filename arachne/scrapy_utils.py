import sys
import logging
from datetime import datetime
from twisted.python import logfile, log as tlog
from scrapy.crawler import Crawler
from scrapy.utils.misc import load_object
from scrapy.settings import Settings
from scrapy.log import ScrapyFileLogObserver


def create_crawler_object(spider_, settings_):
    """
    For the given scrapy settings and spider create a crawler object

    Args:
        spider_ (class obj): The scrapy spider class object
        settings_(class obj): The scrapy settings class object

    Returns:
        A scrapy crawler class object
    """
    crwlr = Crawler(settings_)
    crwlr.configure()
    crwlr.crawl(spider_)
    return crwlr

def start_logger(debug):
    """
    Logger will log for file if debug set to True else will print to cmdline.
    The logfiles will rotate after exceeding since of 1M and 100 count.
    """
    if debug:
        tlog.startLogging(sys.stdout)
    else:
        filename = datetime.now().strftime("%Y-%m-%d.scrapy.log")
        logfile_ = logfile.LogFile(filename, 'logs/', maxRotatedFiles=100)
        logger = ScrapyFileLogObserver(logfile_, logging.INFO)
        tlog.addObserver(logger.emit)

def get_spider_settings(flask_app_config):
    """
    For the given spider_pipelines(dict) create a scrapy Settings object with
    the common settings for each spider/crawler.

    Returns:
        Scrapy settings class instance
    """
    settings = Settings()

    # set the pipelines for exporting to JSON and CSV
    pipelines = {}
    if flask_app_config['EXPORT_JSON']:
        pipelines['arachne.pipelines.ExportJSON'] = 100
    if flask_app_config['EXPORT_CSV']:
        pipelines['arachne.pipelines.ExportCSV'] = 200
    settings.set('ITEM_PIPELINES', pipelines)
    
    return settings

def start_crawler(spider_loc, flask_app_config):
    start_logger(flask_app_config['DEBUG'])
    spider = load_object(spider_loc)
    settings = get_spider_settings(flask_app_config)
    crawler = create_crawler_object(spider(), settings)
    crawler.start()
