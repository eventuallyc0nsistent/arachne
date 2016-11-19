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

Insert item to database
-----------------------
Scrapy allows each of your item to go through your *ITEM_PIPELINES*. We will use the *ITEM_PIPELINES* to insert each of the item scraped to our database using the SQLAlchemy_. In a file called *models.py* paste the following content::

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import scoped_session, sessionmaker
    from sqlalchemy import Column, String, Integer

    # db settings
    dbuser = 'user' #DB username
    dbpass = 'password' #DB password
    dbhost = 'localhost' #DB host
    dbname = 'scrapyspiders' #DB database name
    engine = create_engine("mysql://%s:%s@%s/%s?charset=utf8&use_unicode=0"
                           %(dbuser, dbpass, dbhost, dbname),
                           echo=False,
                           pool_recycle=1800)
    db = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))

    Base = declarative_base()

    class AllData(Base):
        __tablename__ = 'alldata'

        id = Column(Integer, primary_key=True)
        title = Column(String(1000))
        url = Column(String(1000))
        desc = Column(String(3000))

        def __init__(self, id=None, title=None, url=None, desc=None):
            self.id = id
            self.title = title
            self.url = url
            self.desc = desc

        def __repr__(self):
            return "<AllData: id='%d', title='%s', url='%s', desc='%s'>" % (self.id, self.title, self.url, self.desc)

Once you setup the SQLAlchemy *models* you need to add the following code to the *pipelines.py* file::

    from models import AllData, db

    class AddTablePipeline(object):

        def process_item(self, item, spider):

            # create a new SQL Alchemy object and add to the db session
            record = AllData(title=item['title'][0].decode('unicode_escape'),
                             url=item['url'][0],
                             desc=desc)
            db.add(record)
            db.commit()
            return item

Settings
--------
You need to specify the endpoint you would like to run your spider at in your *settings.py* file. To read more about the *SPIDER_SETTINGS* variables goto this link_. It should look like::

    SPIDER_SETTINGS = [
        {
            'endpoint': 'dmoz',
            'location': 'spiders.DmozSpider',
            'spider': 'DmozSpider',
            'scrapy_settings': {
                'ITEM_PIPELINES': {
                    'pipelines.AddTablePipeline': 500
                }
            }    
        }
    ]

Directory Structure
-------------------
So finally this is what your directory should look like::

    .
    ├── app.py
    ├── settings.py
    ├── models.py
    ├── pipelines.py
    └── spiders
        ├── DmozSpider.py
        └── __init__.py # don't forget the __init__.py file

Now, run your application with the python command::

    python app.py



Navigate to the URL http://localhost:8080/ to get a list of the spiders in your project. For the above example you should receive a response as::

    {
        spiders:['dmoz']
    }

To run the *dmoz* spider you can navigate to the URL http://localhost:8080/run-spider/dmoz.

.. note::
   You can also check the full quickstart project on github_.

.. _link: settings.html
.. _github: https://github.com/kirankoduru/arachne-demo
.. _SQLAlchemy: http://www.sqlalchemy.org/
