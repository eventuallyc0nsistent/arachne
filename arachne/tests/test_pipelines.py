"""
To see if we have the right pipelines in place
"""
import inspect
from unittest import TestCase
from mock import patch, mock_open, Mock
from arachne.pipelines import ExportCSV, ExportData, ExportJSON
from scrapy.contrib.exporter import CsvItemExporter, JsonItemExporter

class TestPipelines(TestCase):

    def test_cls_ExportData(self):
        cls = ExportData()
        self.assertTrue(inspect.ismethod(cls.from_crawler))

        with self.assertRaises(NotImplementedError):
            cls.spider_opened('test')

        self.assertEquals(cls.files, {})
        self.assertIsNone(cls.exporter)

    def test_cls_ExportJSON(self):
        cls = ExportJSON()
        mock_open_func = mock_open(read_data='Hello')
        spider = Mock()
        spider.name = 'abc'

        with patch('arachne.pipelines.open', mock_open_func):
            cls.spider_opened(spider)
            mock_open_func.assert_called_with('exports/json/abc.json', 'w+b')
            self.assertIsInstance(cls.exporter, JsonItemExporter)

    def test_cls_ExportCSV(self):
        cls = ExportCSV()
        mock_open_func = mock_open(read_data='Hello')
        spider = Mock()
        spider.name = 'abc'

        with patch('arachne.pipelines.open', mock_open_func):
            cls.spider_opened(spider)
            mock_open_func.assert_called_with('exports/csv/abc.csv', 'w+b')
            self.assertIsInstance(cls.exporter, CsvItemExporter)
