from scrapy import signals
from scrapy import version_info as SCRAPY_VERSION

if SCRAPY_VERSION <= (1, 0, 0):
    from scrapy.contrib.exporter import CsvItemExporter, JsonItemExporter
else:
    from scrapy.exporters import CsvItemExporter, JsonItemExporter

class ExportData(object):

    def __init__(self):
        self.files = {}
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signals.item_scraped)
        return ext

    def spider_opened(self, spider):
        raise NotImplementedError

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file_to_save = self.files.pop(spider)
        file_to_save.close()

    def item_scraped(self, item, spider):
        self.exporter.export_item(item)
        return item

class ExportCSV(ExportData):
    """
    Exporting to export/csv/spider-name.csv file
    """
    def spider_opened(self, spider):
        file_to_save = open('exports/csv/%s.csv' % spider.name, 'w+b')
        self.files[spider] = file_to_save
        self.exporter = CsvItemExporter(file_to_save)
        self.exporter.start_exporting()

class ExportJSON(ExportData):
    """
    Exporting to export/json/spider-name.json file
    """
    def spider_opened(self, spider):
        file_to_save = open('exports/json/%s.json' % spider.name, 'w+b')
        self.files[spider] = file_to_save
        self.exporter = JsonItemExporter(file_to_save)
        self.exporter.start_exporting()
