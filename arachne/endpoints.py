from flask import current_app as app, jsonify, abort
from arachne.scrapy_utils import start_crawler

def list_spiders_endpoint():
    """It returns a list of spiders available in the SPIDER_SETTINGS dict 
    """
    spiders = []
    for item in app.config['SPIDER_SETTINGS']:
        spiders.append(item['endpoint'])
    return jsonify(endpoints=spiders)

def run_spider_endpoint(spider_name):
    """Search for the spider_name in the SPIDER_SETTINGS dict and
    start running the spider with the Scrapy API"""

    for item in app.config['SPIDER_SETTINGS']:
        if spider_name in item['endpoint']:
            spider_loc = '%s.%s' % (item['location'], item['spider'])
            start_crawler(spider_loc, app.config, item.get('scrapy_settings'))
            return jsonify(status='<%s> running'% spider_name)
    return abort(404)
