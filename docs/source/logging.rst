.. _logging:

Logging
=======
There are 2 types of logs that you can work with in this project. One will be the HTTP logs for your *Flask* application and the next one will be your *Scrapy* spider.


Flask logs
----------
By default HTTP logging is disabled for the *Flask* application. To turn on logging to a file please set the ``LOGS`` variable in *settings.py* to ``True``.

Scrapy logs
-----------
*Scrapy* logs for spiders are very important to know exactly what is going on. The *Scrapy* logs are turned on by default for ``stdout`` but to log to a file set the ``DEBUG`` variable in your *settings.py* to ``False``.
