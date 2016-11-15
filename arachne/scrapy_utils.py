from scrapy.utils.misc import load_object
from scrapy.settings import Settings


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

    if 'ITEM_PIPELINES' not in all_settings:
        all_settings['ITEM_PIPELINES'] = {}

    if flask_app_config['EXPORT_JSON']:
        all_settings['ITEM_PIPELINES']['arachne.extensions.ExportJSON'] = 100

    if flask_app_config['EXPORT_CSV']:
        all_settings['ITEM_PIPELINES']['arachne.extensions.ExportCSV'] = 200

    # spider scrapy settings has priority over global scrapy settings
    for setting, _ in all_settings.items():
        if spider_scrapy_settings and setting in spider_scrapy_settings:
            all_settings[setting].update(spider_scrapy_settings[setting])

    settings = Settings(all_settings)
    return settings


def start_crawler(spider_loc, flask_app_config, spider_scrapy_settings):
    spider = load_object(spider_loc)
    settings = get_spider_settings(flask_app_config, spider_scrapy_settings)
    spider.custom_settings = settings
    flask_app_config['CRAWLER_PROCESS'].crawl(spider)
