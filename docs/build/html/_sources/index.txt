Python Flask Scrapy API 
=======================

Arachne provides a wrapper around your scrapy spider to run them through a flask app. All you have to do is setup your ``SPIDER_SETTINGS`` in the settings file. You can view the source code on `github <https://github.com/kirankoduru/arachne>`_.

Arachne is powered by Flask_, Twisted_ and the Scrapy_ package

Why not scrapyd?
----------------
`The best code is no code at all`_, I have tried to write as little code as possible to maintain my scrapy projects but when I started off using scrapy daemon, it was incredibly harder to maintain. My project grew to over 100 spiders and then I started to break my projects into smaller tiny pieces when I got to the bare roots of it then *lo and behold*, this project is its creation. 

Installation
------------
To install Arachne from pip use the command

	pip install -i https://pypi.python.org/pypi/Arachne 

Getting started
---------------
Learn more about getting start quickly in the `guide`_.

.. toctree::
	:hidden:

	quickstart
	settings
	logging
	changelog

.. _Flask: https://github.com/mitsuhiko/flask/
.. _Twisted:  https://twistedmatrix.com/trac/
.. _Scrapy: https://github.com/scrapy/scrapy/
.. _guide: quickstart.html
.. _The best code is no code at all: http://blog.codinghorror.com/the-best-code-is-no-code-at-all/
