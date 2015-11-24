.. _spider_settings:

Settings
========

Since this project depends both on Flask_ and Scrapy_, you can mention the individual settings for each in the *settings.py*. 

Global settings
---------------
You can set the global settings for Flask_ and Scrapy_ through these variables:

=================== ===========
Field               Description
=================== ===========
``USER_AGENT``  	Crawl responsibly. Set the ``USER_AGENT`` variable for each spider. Default set to ``Arachne (+http://github.com/kirankoduru/arachne)``
``EXPORT_PATH`` 	Set the export path for your *json* and *csv* files. Default set to ``exports/`` directory
``LOGS_PATH``   	Set the logs path for your spiders. Default set to ``logs/`` directory. Each day is logged in the datetime file ``%Y-%m-%d.scrapy.log``
``EXPORT_JSON`` 	Turn *json* exporting for all spiders ON(``True``) or OFF(``False``). Default set to ``False``
``EXPORT_CSV``  	Turn *csv* exporting for all spiders ON(``True``) or OFF(``False``). Default set to ``False``
``LOGS``        	Turn ON(``True``) or off(``False``) HTTP logging for your flask app. Default set to ``False``
``SCRAPY_SETTINGS`` Set `scrapy settings`_ that you would like to set globally for each individual spider
=================== ===========

Spider settings
---------------
You can customize each spider with by modifying the *SPIDER_SETTINGS* variable in *settings.py* file. For the initial release you can set the following settings for each spider:

=================== ==========================================================
Field               Description
=================== ==========================================================
``endpoint``        The URL endpoint that you would like to associate with the spider.
``location``        The spider location is usally the module location to the spider in a dot notation. Consider that your *DmozSpider* is in the *spiders* directory, then the ``location`` variable will be set to **spiders.DmozSpider**.
``spider``          The ``class`` name of the *Spider*.
``scrapy_settings`` This will let you override the individual settings for each spider in the scrapers. You can add scrapy pipelines or extensions through this variable. This setting takes priority over your global ``SCRAPY_SETTINGS`` field
=================== ==========================================================

.. note::
   You can override all the Flask_ settings from the *settings.py* file. View the list of `scrapy settings`_ you can use.

.. _Flask: https://github.com/mitsuhiko/flask/
.. _Scrapy: https://github.com/scrapy/scrapy/
.. _scrapy settings: http://doc.scrapy.org/en/0.24/topics/settings.html
