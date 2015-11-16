import os
import sys
from flask import Flask

from arachne.exceptions import SettingsException
from arachne.endpoints import list_spiders_endpoint, run_spider_endpoint

class Arachne(Flask):

    def __init__(self, import_name=__package__, 
                 settings='settings.py', **kwargs):
        """Initialize the flask app with the settings variable. Load config
        from the settings variable and test if the all the 
        directories(for exports & logs) exists. Finally bind the endpoints for
        the flask application to control the spiders
        """
        super(Arachne, self).__init__(import_name, **kwargs)
        self.settings = settings

        self.load_config()
        self.validate_spider_settings()

        # create directories
        self.check_dir_json()
        self.check_dir_csv()
        self.check_dir_logs()

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

    def check_dir_json(self):
        """Create json export directory on EXPORT_JSON True
        """
        if self.config['EXPORT_JSON']:
            check_dir(self.config['EXPORT_PATH'], 'json/')

    def check_dir_csv(self):
        """Create csv export directory on EXPORT_CSV True
        """
        if self.config['EXPORT_CSV']:
            check_dir(self.config['EXPORT_PATH'], 'csv/')

    def check_dir_logs(self):
        """Create logs directory on LOGS True
        """
        if self.config['LOGS']:
            check_dir(self.config['LOGS_PATH'], '')

    def validate_spider_settings(self):
        try:
            spider_settings = self.config['SPIDER_SETTINGS']
        except:
            raise SettingsException('SPIDER_SETTINGS missing')
        if not isinstance(spider_settings, list):
            raise SettingsException('SPIDER_SETTINGS must be a dict')

    def _init_url_rules(self):
        """Attach the endpoints to run spiders and list the spiders
        that are available in the API
        """
        self.add_url_rule('/run-spider/<spider_name>', view_func=run_spider_endpoint)
        self.add_url_rule('/spiders/', view_func=list_spiders_endpoint)

def check_dir(path, folder):
    """Check if directory exists else raise exception
    """ 
    cwd = os.getcwd()
    export_dir = cwd+'/'+path+folder
    if not os.path.exists(export_dir):
        raise SettingsException('Directory missing ', export_dir)
