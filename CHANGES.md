Changelog
=========

Here you will find the full list of changes between each Arachne release


Version 0.5.0 (Nov 20th 2016)
---------------------
- Add support for Scrapy 1.0 ([#4](https://github.com/kirankoduru/arachne/issues/4))

Version 0.4.0 (Mar 17th 2016)
-----------------------------
- Renamed the endpoints `/spiders` as `/` for more intuitive purposes - ([#8](https://github.com/kirankoduru/arachne/issues/8))
- The `/run-spider` endpoint returns the name of spider and the status of the spider as running

Version 0.3.1 (Nov 25th 2015)
-----------------------------
- [BUG FIX] Whoops! Forgot to test if there were individual spider `scrapy_settings` available

Version 0.3.0 (Nov 23rd 2015)
-----------------------------
- Add individual spider settings to the `scrapy_settings` variable 
- Add global spider settings to the `SCRAPY_SETTINGS` variable 

Version 0.2.0 (Nov 15th 2015)
-----------------------------
- Export to CSV and JSON pipeline now available 

Version 0.1.0 (Nov 14th 2015)
-----------------------------
- First public preview release
