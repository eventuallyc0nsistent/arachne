import os
import sys
from flask import Flask
from arachne.exceptions import SettingsException
from arachne.endpoints import spider_endpoint

class Arachne(Flask):

    def __init__(self, import_name=__package__, 
                 settings='settings.py', **kwargs):

        super(Arachne, self).__init__(import_name, **kwargs)
        self.settings = settings

        self.load_config()
        self.validate_spider_settings()

        # create directories
        self.mkdir_json()
        self.mkdir_csv()
        self.mkdir_logs()

        self._init_url_rules()

    def run(self, host=None, port=None, debug=None, **options):
        super(Arachne, self).run(host, port, debug, **options)

    def load_config(self):
        """Default settings are loaded first and then overwritten from
        personal `settings.py` file
        """ 
        self.config.from_object('arachne.default_settings')

        if isinstance(self.settings, dict):
            self.config.update(self.settings)
        else:
            if os.path.isabs(self.settings):
                pyfile = self.settings
            else:
                abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
                pyfile = os.path.join(abspath, self.settings)
            try:
                self.config.from_pyfile(pyfile)
            except IOError:
                # assume envvar is going to be used exclusively
                pass
            except:
                raise

        # overwrite settings with custom environment variable
        envvar = 'ARACHNE_SETTINGS'
        if os.environ.get(envvar):
            self.config.from_envvar(envvar)

    def mkdir_json(self):
        """Create json export directory on EXPORT_JSON True
        """
        if self.config['EXPORT_JSON']:
            self.create_dir(self.config['EXPORT_PATH'], 'json/')

    def mkdir_csv(self):
        """Create csv export directory on EXPORT_CSV True
        """
        if self.config['EXPORT_JSON']:
            self.create_dir(self.config['EXPORT_PATH'], 'csv/')

    def mkdir_logs(self):
        """Create logs directory on LOGS True
        """
        if self.config['LOGS']:
            self.create_dir(self.config['LOGS_PATH'], '')

    def validate_spider_settings(self):
        try:
            spider_settings = self.config['SPIDER_SETTINGS']
        except:
            raise SettingsException('SPIDER_SETTINGS missing')
        if not isinstance(spider_settings, list):
            raise SettingsException('SPIDER_SETTINGS must be a dict')

    def _init_url_rules(self):
        self.add_url_rule('/spiders', 'spiders', spider_endpoint)

    def create_dir(self, path, folder):
        """Create a directory in the current working directory
        """ 
        cwd = os.getcwd()
        export_dir = cwd+'/'+path+folder
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
