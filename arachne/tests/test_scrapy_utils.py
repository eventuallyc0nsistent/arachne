import sys
from unittest import TestCase
from datetime import datetime
from mock import Mock, patch
from scrapy import version_info as SCRAPY_VERSION
from scrapy.settings import Settings
from arachne.scrapy_utils import (create_crawler_object, start_logger,
                                  get_spider_settings, start_crawler)

def get_flask_export_config(bool_json, bool_csv):
    """Return dict with the boolean set for EXPORT params
    """
    return {
        'DEBUG': True,
        'EXPORT_JSON': bool_json,
        'EXPORT_CSV': bool_csv, 
        'SCRAPY_SETTINGS': {}
    }

def get_item_export_extension(bool_json, bool_csv):
    extensions = {}
    if bool_json:
        extensions['arachne.extensions.ExportJSON'] = 100
    if bool_csv:
        extensions['arachne.extensions.ExportCSV'] = 200
    return extensions

class TestScrapyUtils(TestCase):

    def setUp(self):
        self.spider = Mock()
        self.settings = Settings()

    def test_create_crawler_object(self):
        if SCRAPY_VERSION <= (1, 0, 0):
            from scrapy.crawler import Crawler
            crwlr = create_crawler_object(self.spider, self.settings)
            self.assertIsInstance(crwlr, Crawler)

    def test_create_crawler_mock(self):
        if SCRAPY_VERSION <= (1, 0, 0):
            with patch('arachne.scrapy_utils.Crawler') as mock_crawler:
                create_crawler_object(self.spider, self.settings)
                mock_crawler.assert_called_with(self.settings)

    def test_start_logger(self):
        if SCRAPY_VERSION <= (1, 0, 0):
            with patch('arachne.scrapy_utils.tlog') as mock_twisted_log:
                start_logger(True)
                self.assertTrue(mock_twisted_log.is_called)
                mock_twisted_log.startLogging.assert_called_with(sys.stdout)

            with patch('arachne.scrapy_utils.logfile') as mock_twisted_logfile:
                start_logger(False)
                y_m_d_date = datetime.now().strftime('%Y-%m-%d.scrapy.log')
                self.assertTrue(mock_twisted_logfile.is_called)
                mock_twisted_logfile.LogFile.assert_called_with(
                        y_m_d_date, 'logs/', maxRotatedFiles=100)

    def test_get_spider_settings(self):
        bool_json_csv = [
            (True, True),
            (True, False),
            (False, True),
            (False, False)
        ]

        for item in bool_json_csv:
            test_flask_config = get_flask_export_config(item[0], item[1])
            extensions = get_item_export_extension(item[0], item[1])
            settings = get_spider_settings(test_flask_config, {})
            self.assertIsInstance(settings, Settings)
            self.assertEquals(settings.get('EXTENSIONS'), extensions)

            # test if global settings are appeneded to spider settings 
            test_flask_config['SCRAPY_SETTINGS']['EXTENSIONS'] = {
                'apple': 100,
                'batman': 200
            }
            extensions.update(
                test_flask_config['SCRAPY_SETTINGS']['EXTENSIONS'])
            settings = get_spider_settings(test_flask_config, {})
            self.assertEquals(settings['EXTENSIONS'], extensions)

            # test if spider settings have priority over scrapy settings
            test_flask_config = get_flask_export_config(item[0], item[1])
            extensions = get_item_export_extension(item[0], item[1])
            spider_settings = {
                'EXTENSIONS': {
                    'arachne.extensions.ExportJSON': 300,
                    'arachne.extensions.ExportCSV': 400,
                }
            }
            settings = get_spider_settings(test_flask_config, spider_settings)
            self.assertEquals(settings.get('EXTENSIONS'), 
                              spider_settings['EXTENSIONS'])

    def test_start_crawler(self):
        if SCRAPY_VERSION <= (1, 0, 0):
            with patch('arachne.scrapy_utils.tlog') as tlog:
                with patch('arachne.scrapy_utils.load_object') as load_object:
                    with patch('arachne.scrapy_utils.Crawler') as _:
                        spider_loc = 'ABC.ABC'
                        flask_app_config = get_flask_export_config(True, True)
                        spider_scrapy_settings = {
                            'EXTENSIONS': get_item_export_extension(False, True)
                        }
                        start_crawler(spider_loc, 
                                      flask_app_config, 
                                      spider_scrapy_settings)

                        assert tlog.startLogging.called
                        load_object.assert_called_with(spider_loc)

