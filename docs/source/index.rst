Python Flask Scrapy API 
=======================

Arachne provides a wrapper around your scrapy spider to run them through a flask app. All you have to do is setup your ``SPIDER_SETTINGS`` in the settings file. You can view the source code on `github <https://github.com/kirankoduru/arachne>`_.

Arachne is powered by Flask_, Twisted_ and the Scrapy_ package


Installation
------------
You can install **Arachne** from pip 

	pip install arachne



Sample settings
---------------
This is sample settings file for spiders in your project. The settings file should be called **settings.py** for **Arachne** to find it and looks like this::

	SPIDER_SETTINGS = [
		{
			'endpoint': 'dmoz',
			'location': 'spiders.DmozSpider',
			'spider': 'DmozSpider'    
		}
	]

Usage
-----
It looks very similar to a flask app but since **Scrapy** depends on the python **twisted** package, we need to run our flask app with **twisted**::

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

The API is running. Navigate to http://localhost:8080/spiders to get the list of spiders you can run

.. toctree::
	:hidden:

	config
	quickstart

.. _Flask: https://github.com/mitsuhiko/flask/
.. _Twisted:  https://twistedmatrix.com/trac/
.. _Scrapy: https://github.com/scrapy/scrapy/
