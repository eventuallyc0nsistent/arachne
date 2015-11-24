import sys
from unittest import TestCase
from datetime import datetime
from mock import Mock, patch
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from arachne.scrapy_utils import create_crawler_object, start_logger, get_spider_settings

class TestScrapyUtils(TestCase):

    def setUp(self):
        self.spider = Mock()
        self.settings = Settings()

    def test_create_crawler_object(self):
        crwlr = create_crawler_object(self.spider, self.settings)
        self.assertIsInstance(crwlr, Crawler)

    @patch('arachne.scrapy_utils.Crawler')
    def test_create_crawler_mock(self, mock_Crawler):
        create_crawler_object(self.spider, self.settings)
        mock_Crawler.assert_called_with(self.settings)

    @patch('arachne.scrapy_utils.logfile')
    @patch('arachne.scrapy_utils.tlog')
    def test_start_logger(self, mock_twisted_log, mock_twisted_logfile):
        start_logger(True)
        self.assertTrue(mock_twisted_log.is_called)
        mock_twisted_log.startLogging.assert_called_with(sys.stdout)

        start_logger(False)
        YmD_date = datetime.now().strftime('%Y-%m-%d.scrapy.log')
        self.assertTrue(mock_twisted_logfile.is_called)
        mock_twisted_logfile.LogFile.assert_called_with(YmD_date, 'logs/', maxRotatedFiles=100)

    def get_flask_export_config(self, bool_json, bool_csv):
        """Return dict with the boolean set for EXPORT params
        """
        return {
            'EXPORT_JSON': bool_json,
            'EXPORT_CSV': bool_csv, 
            'SCRAPY_SETTINGS': {}
        }

    def get_item_export_pipeline(self, bool_json, bool_csv):
        pipelines = {}
        if bool_json:
            pipelines['arachne.pipelines.ExportJSON'] = 100
        if bool_csv:
            pipelines['arachne.pipelines.ExportCSV'] = 200
        return pipelines

    def test_get_spider_settings(self):
        bool_json_csv = [
            (True, True),
            (True, False),
            (False, True),
            (False, False)
        ]

        for item in bool_json_csv:
            test_flask_config = self.get_flask_export_config(item[0], item[1])
            pipelines = self.get_item_export_pipeline(item[0], item[1])
            settings = get_spider_settings(test_flask_config, {})
            self.assertIsInstance(settings, Settings)
            self.assertEquals(settings.get('ITEM_PIPELINES'), pipelines)
