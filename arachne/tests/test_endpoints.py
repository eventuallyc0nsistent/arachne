"""
Testing the endpoints called with the API
"""

import json
from mock import patch
from arachne.tests.BaseFlaskApp import BaseFlaskApp

class TestFlaskEndpoints(BaseFlaskApp):

    def test_list_spiders_endpoint(self):
        resp = self.client.get('/')
        expected_resp = {
            'endpoints': {
                'abc': 'http://localhost/run-spider/abc',
                'pqr': 'http://localhost/run-spider/pqr'
            }
        }
        self.assertTrue(resp.data, expected_resp)

    @patch('arachne.endpoints.start_crawler')
    def test_run_spider_endpoint(self, mock_start_crawler):
        resp = self.client.get('/run-spider/abc')
        self.assertTrue(mock_start_crawler.called)
        client_config = self.client.application.config
        mock_start_crawler.assert_called_once_with('spiders.abc.ABC.ABC', 
                                                   client_config, 
                                                   {'TELNETCONSOLE_PORT': 2020})

        self.assertEquals(json.loads(resp.data), 
                          {'home': 'http://localhost/', 
                           'status': 'running', 
                           'spider_name': 'abc'})

        resp = self.client.get('/run-spider/xyz')
        self.assertEquals(404, resp.status_code)
