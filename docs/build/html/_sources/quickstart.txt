.. _quickstart:

Quickstart
==========

To be able to run your spiders from the Flask API need to create the following files


Create flask app
----------------
Create a file called *app.py* with the following code::

	from twisted.web.wsgi import WSGIResource
	from twisted.web.server import Site
	from twisted.internet import reactor
	from arachne import Arachne

	app = Arachne(__name__)

	resource = WSGIResource(reactor, reactor.getThreadPool(), app)
	site = Site(resource)
	reactor.listenTCP(8080, site)

	if __name__ == '__main__':
		reactor.run()


Spider
------
Lets say we have a spider that crawls http://dmoz.org that looks like::

	import scrapy

	class DmozItem(scrapy.Item):
		"""Item object to store title, link, description"""

		title = scrapy.Field()
		url = scrapy.Field()
		desc = scrapy.Field()

	class DmozSpider(scrapy.Spider):
		"""
		Spider to crawl Python books and resources on dmoz.org
		"""
		name = "dmoz"
		allowed_domains = ["dmoz.org"]
		start_urls = [
			"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
			"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
		]

		def parse(self, response):
			for sel in response.xpath('//ul/li'):
				item = DmozItem()
				item['title'] = sel.xpath('a/text()').extract()
				item['url'] = sel.xpath('a/@href').extract()
				item['desc'] = sel.xpath('text()').extract()
				yield item


Settings
--------
You need to specify the endpoint you would like to run your spider at in your *settings.py* file. To read more about the *SPIDER_SETTINGS* variables goto this link_. It should look like::

	SPIDER_SETTINGS = [
		{
			'endpoint': 'dmoz',
			'location': 'spiders.DmozSpider',
			'spider': 'DmozSpider'    
		}
	]

Directory Structure
-------------------
So finally this is what your directory should look like::

	.
	├── app.py
	├── settings.py
	└── spiders
		├── DmozSpider.py
		└── __init__.py # don't forget the __init__.py file

Now, run your application with the python command::

	python app.py


.. _link: settings.html

Navigate to the URL http://localhost:8080/spiders/ to get a list of the spiders in your project. For the above example you should receive a response as::

	{
		spiders:['dmoz']
	}

To run the *dmoz* spider you can navigate to the URL http://localhost:8080/run-spider/dmoz.
