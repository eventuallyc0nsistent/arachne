from os import getcwd
from arachne.flaskapp import Arachne
from scrapy import version_info as SCRAPY_VERSION
from flask.config import Config
from flask import Flask
from unittest import TestCase


class TestFlaskApp(TestCase):

    def create_app(self, settings):
        app = Arachne(__name__, settings=settings)
        return app

    def test_settings_dict(self):
        """Check if the config obj is updated with default_settings values when
        it passed as a dict
        """
        settings = {
            'SPIDER_SETTINGS': [{
                'endpoint': 'abc',
                'location': 'spiders.abc.ABC',
                'spider': 'ABC',
                'scrapy_settings': {
                    'TELNETCONSOLE_PORT': 2020
                }
            }, {
                'endpoint': 'pqr',
                'location': 'spiders.pqr.PQR',
                'spider': 'PQR',
            }],
            'SECRET_KEY' : 'secret_test_key',
            'TESTING': True,
            'SCRAPY_SETTINGS': {
                'TELNETCONSOLE_PORT': 3030
            }
        }
        app = self.create_app(settings)

        # since the object initialized created is always different
        # we ignore CRAWLER_PROCESS setting for test
        if SCRAPY_VERSION >= (1, 0, 0):
            del app.config['CRAWLER_PROCESS']

        # default flask app with config updated with arachne.default_settings
        default_flask_app = Flask(__name__)
        default_flask_app.config.from_object('arachne.default_settings')
        default_flask_app.config.update(settings)
        self.assertEquals(app.config, default_flask_app.config)
 
    def test_settings_abs_path(self):
        """Check if the config obj is updated with default_settings when it is 
        passed as a python file absolute path
        """
        abs_path = getcwd() + '/arachne/tests/test_settings.py'
        test_app = self.create_app(settings=abs_path)

        # since the object initialized created is always different
        # we ignore CRAWLER_PROCESS setting for test
        if SCRAPY_VERSION >= (1, 0, 0):
            del test_app.config['CRAWLER_PROCESS']

        # load config from pyfile
        flask_app = Flask(__name__)
        flask_app.config.from_object('arachne.default_settings')

        config_cls = Config(__name__)
        config_cls.from_pyfile(abs_path)

        # update config with the arachne default settings
        flask_app.config.update(config_cls)

        # test if config dicts are same
        self.assertEquals(test_app.config, flask_app.config)
