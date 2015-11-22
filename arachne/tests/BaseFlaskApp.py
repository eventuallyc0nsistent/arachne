"""
BaseTestCase 
"""
from arachne.flaskapp import Arachne
from unittest import TestCase

class BaseFlaskApp(TestCase):
    """
    Create test client app with a test secret key
    """

    def setUp(self):
        """
        sample SPIDER_SETTINGS for tests
        """
        settings = {
            'SPIDER_SETTINGS': [{
                'endpoint': 'abc',
                'location': 'spiders.abc.ABC',
                'spider': 'ABC',
            }],
            'SECRET_KEY' : 'secret_test_key',
            'TESTING': True
        }
        self.app = Arachne(__name__, settings=settings)
        self.client = self.app.test_client()

    def tearDown(self):
        del self.app
