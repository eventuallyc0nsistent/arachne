from scrapy.crawler import Crawler
from scrapy.settings import Settings

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

def get_spider_settings():
    """
    For the given spider_pipelines(dict) create a scrapy Settings object with
    the common settings for each spider/crawler.

    Returns:
        Scrapy settings class instance
    """
    settings = Settings()
    pipelines = {
        'helpers.pipelines.ExportCSV': 100,
        'helpers.pipelines.ExportJSON': 200,
    }
    extensions = {
        'helpers.extensions.StatsCollectorExt': 200,
    }
    settings.set("TELNETCONSOLE_PORT", None)
    settings.set("DOWNLOAD_TIMEOUT", 800)
    settings.set("ITEM_PIPELINES", pipelines)
    settings.set("EXTENSIONS", extensions)
    settings.set("USER_AGENT", "Kiran Koduru (+http://github.com/kirankoduru)")

    return settings

def start_crawler(endpoint):
    
