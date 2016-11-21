from scrapy import version_info as SCRAPY_VERSION
from scrapy.utils.misc import load_object
from scrapy.settings import Settings

if SCRAPY_VERSION <= (1, 0, 0):
    import sys
    import logging
    from datetime import datetime
    from twisted.python import logfile, log as tlog
    from scrapy.crawler import Crawler
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

def get_spider_settings(flask_app_config, spider_scrapy_settings):
    """
    For the given settings for each spider create a scrapy Settings object with
    the common settings spider & its personal settings. Individual spider scrapy
    settings takes priority over global scrapy settings

    Returns:
        Scrapy settings class instance

    .. version 0.3.0:
       Allow settings for individual spiders and global settings
    """
    all_settings = flask_app_config['SCRAPY_SETTINGS']

    if 'EXTENSIONS' not in all_settings:
        all_settings['EXTENSIONS'] = {}

    if flask_app_config['EXPORT_JSON']:
        all_settings['EXTENSIONS']['arachne.extensions.ExportJSON'] = 100

    if flask_app_config['EXPORT_CSV']:
        all_settings['EXTENSIONS']['arachne.extensions.ExportCSV'] = 200

    # spider scrapy settings has priority over global scrapy settings
    for setting, _ in all_settings.items():
        if spider_scrapy_settings and setting in spider_scrapy_settings:
            all_settings[setting].update(spider_scrapy_settings[setting])

    settings = Settings(all_settings)
    return settings


def start_crawler(spider_loc, flask_app_config, spider_scrapy_settings):
    spider = load_object(spider_loc)
    settings = get_spider_settings(flask_app_config, spider_scrapy_settings)

    if SCRAPY_VERSION <= (1, 0, 0):
        start_logger(flask_app_config['DEBUG'])
        crawler = create_crawler_object(spider(), settings)
        crawler.start()

    else:
        spider.custom_settings = settings
        flask_app_config['CRAWLER_PROCESS'].crawl(spider)

