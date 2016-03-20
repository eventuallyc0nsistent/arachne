import sys
from unittest import TestCase
from datetime import datetime
from mock import Mock, patch
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from arachne.scrapy_utils import (create_crawler_object, start_logger,
                                  get_spider_settings, start_crawler)

class TestScrapyUtils(TestCase):

    def setUp(self):
        self.spider = Mock()
        self.settings = Settings()

    def test_create_crawler_object(self):
        crwlr = create_crawler_object(self.spider, self.settings)
        self.assertIsInstance(crwlr, Crawler)

    @patch('arachne.scrapy_utils.Crawler')
    def test_create_crawler_mock(self, mock_crawler):
        create_crawler_object(self.spider, self.settings)
        mock_crawler.assert_called_with(self.settings)

    @patch('arachne.scrapy_utils.logfile')
    @patch('arachne.scrapy_utils.tlog')
    def test_start_logger(self, mock_twisted_log, mock_twisted_logfile):
        start_logger(True)
        self.assertTrue(mock_twisted_log.is_called)
        mock_twisted_log.startLogging.assert_called_with(sys.stdout)

        start_logger(False)
        y_m_d_date = datetime.now().strftime('%Y-%m-%d.scrapy.log')
        self.assertTrue(mock_twisted_logfile.is_called)
        mock_twisted_logfile.LogFile.assert_called_with(y_m_d_date, 
                                                        'logs/', 
                                                        maxRotatedFiles=100)

    def get_flask_export_config(self, bool_json, bool_csv):
        """Return dict with the boolean set for EXPORT params
        """
        return {
            'DEBUG': True,
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

            # test if global settings are appeneded to spider settings 
            test_flask_config['SCRAPY_SETTINGS']['ITEM_PIPELINES'] = {
                'apple': 100,
                'batman': 200
            }
            pipelines.update(test_flask_config['SCRAPY_SETTINGS']['ITEM_PIPELINES'])
            settings = get_spider_settings(test_flask_config, {})
            self.assertEquals(settings['ITEM_PIPELINES'], pipelines)

            # test if spider settings have priority over scrapy settings
            test_flask_config = self.get_flask_export_config(item[0], item[1])
            pipelines = self.get_item_export_pipeline(item[0], item[1])
            spider_settings = {
                'ITEM_PIPELINES': {
                    'arachne.pipelines.ExportJSON': 300,
                    'arachne.pipelines.ExportCSV': 400,
                }
            }
            settings = get_spider_settings(test_flask_config, spider_settings)
            self.assertEquals(settings.get('ITEM_PIPELINES'), spider_settings['ITEM_PIPELINES'])

    @patch('arachne.scrapy_utils.Crawler')
    @patch('arachne.scrapy_utils.load_object')
    @patch('arachne.scrapy_utils.tlog')
    def test_start_crawler(self, tlog, load_object, crwlr):
        spider_loc = 'ABC.ABC'
        flask_app_config = self.get_flask_export_config(True, True)
        spider_scrapy_settings = {
            'ITEM_PIPELINES': self.get_item_export_pipeline(False, True)
        }
        start_crawler(spider_loc, flask_app_config, spider_scrapy_settings)

        assert tlog.startLogging.called
        load_object.assert_called_with(spider_loc)

