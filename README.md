## Description

This example allows you to get the current price of SP500 CFD using the web scraping technique.

## Web Scraping
In general, web scraping is the process by which, extracting data from the web, you can analyze that data and turn 
it into useful information. To extract any HTML element, you only need to know the tags that surround it,
as we'll see later.

### Static Scraping vs. Dynamic Scraping
Static scraping ignores JavaScript. It fetches web pages from the server without the use of a browser.
You get exactly what you see in "view page source", and then you could slice and dice it. 
For static scraping I use two Python libraries: [Requests](https://requests.readthedocs.io/en/master/) for fetching web
pages and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for parsing HTML pages,
over [IG Markets Ltd](https://www.ig.com/es/indices/mercado-indices/us-spx-500) site

However, if the final page content depend of parts that get load dynamically with Ajax or JavaScript, the scraper won't
load any of this content as the scraper doesn't execute the JavaScript required to load it. You need dynamic scraping.
For dynamic scraping I use [Selenium](http://www.seleniumframework.com/python-basic/what-is-selenium/) library, 
over [Trading View](https://www.tradingview.com/symbols/FX-SPX500/) site

Dynamic scraping uses an actual browser (or a headless browser) and lets JavaScript do its thing.
Then, it queries the DOM to extract the content it's looking for. 

### Choose your web driver for dynamic scraping
The Selenium library does not include its own browser. It need a third party browser (or a web driver) 
in order to operate, the browser it automates. This is in addition to the browser itself, of course.
You can choose from Chrome, Firefox, Safari or Edge, follow the instructions in the [Selenium guide](https://selenium-python.readthedocs.io/installation.html#drivers).
The driver (.exe file) must be placed on the PATH of your operating system, or the current working folder.
I use [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) in headless mode, which means no UI is displayed.

## Requirements
```console
$ python --version  
Python 3.7.1  
$ pip install -r requirements.txt  
beautifulsoup4==4.9.0  
requests==2.23.0  
selenium==3.141.0  
```