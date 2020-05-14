# Beautiful Soup: library designed for quick turnaround projects like screen-scraping
from bs4 import BeautifulSoup
# Contextlib: this module provides utilities for common tasks involving the 'with' statement
import contextlib
# Requests: library that allows to make HTTP requests
import requests
# Selenium: library to automate the Internet browser and interact with the DOM interactively, it is primarily geared
#   towards automated testing of web applications, but it is great as a general-purpose browser automation tool
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def static_scraping(url_: str,
                    verbose_: bool = False) -> float:
    """
    Attempts to get the static content at `url` by making an HTTP GET request.
    Internally uses Requests and BeautifulSoup libraries.

    :param url_: URL to request
    :param verbose_: flag to show, or not, the page content

    :return: If the content-type of response is some kind of HTML and parse is successful, return the current price,
                otherwise return a zero.
    """
    # Initialize output variable
    extracted_price_ = 0
    markup_to_parse_ = b''

    try:
        # contextlib.closing(thing) return a context manager that closes thing upon completion of the block
        with contextlib.closing(requests.get(url_, stream=True)) as response_:
            if __is_good_response(response_, verbose_):
                # Getting a successful response for parse
                markup_to_parse_ = response_.content.decode('utf-8')

        if len(markup_to_parse_) > 0:
            """
                Available parser libraries for use
                - lxml        : Very fast, lenient, external C dependency
                - html.parser : Decent speed, lenient
                - html5lib    : Very slow, extremely lenient, parses pages as a web browser does, 
                                creates valid HTML5, external Python dependency

                Visit: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser  
            """
            parser_to_use_ = 'html.parser'

            # Parse markup
            html_ = BeautifulSoup(markup_to_parse_, parser_to_use_)

            # We need to find <div class="price-ticket__price" data-field="OFR">, because there is the Ask price.
            # Set attributes of the <div> in a dictionary, to find it
            attributes_to_find_ = {
                'class': 'price-ticket__price',
                'data-field': 'OFR'
            }

            # Seek <div>
            div_ = html_.find('div', attributes_to_find_)

            # Extract current price
            extracted_price_ = float(div_.text)

    except Exception as exception_:
        __log_error(f'Error during request and parse of {url_}\n{type(exception_).__name__}\n{str(exception_)}')

    return extracted_price_


# Internal method
def __is_good_response(response_: requests.Response,
                       verbose_: bool = False) -> bool:
    """
    Evaluate response to check if seems to be HTML

    :param response_: received from a request
    :param verbose_: flag to show, or not, the page content

    :return: True if the response seems to be HTML, False otherwise.
    """
    # Evaluate response
    content_type_ = response_.headers['Content-Type'].lower()
    result_ = (response_.status_code == 200
               and content_type_ is not None
               and content_type_.find('html') > -1)

    if verbose_ and result_:
        # Show page content. BeautifulSoup4 prettify() gives the visual representation of the parse tree created
        #   from the raw HTML content
        print(BeautifulSoup(response_.content, 'html.parser').prettify())

    return result_


def dynamic_scraping(url_: str,
                     verbose_: bool = False) -> float:
    """
    Attempts to get the dynamic content at `url` by using an actual browser and lets JavaScript do its thing.
    Internally uses Selenium library and Chrome web driver.

    :param url_: URL to request
    :param verbose_: flag to show, or not, the page content

    :return: If the content-type of response is some kind of HTML and parse is successful, return the current price,
                otherwise return a zero.
    """

    # Initialize output variable
    extracted_price_ = 0

    # Set options to execute browser
    browser_options_ = Options()
    # Enable headless mode, which means no UI is displayed
    browser_options_.headless = True

    # Create an instance of the Chrome driver, the executable_path points to the executable;
    #   if not specified, it assumes the executable is in the main script folder or in the PATH.
    driver = Chrome(options=browser_options_, executable_path='chromedriver.exe')

    try:
        driver.get(url_)

        if verbose_:
            # Show page content. BeautifulSoup4 prettify() gives the visual representation of the parse tree created
            #   from the raw HTML content
            print(BeautifulSoup(driver.page_source.encode("utf-8"), 'html.parser').prettify())
            # print(driver.page_source)

        # We need to find <div class="tv-symbol-price-quote__value js-symbol-last">, because there is the last price.
        class_name_ = 'tv-symbol-price-quote__value'
        div_ = driver.find_element_by_class_name(class_name_)

        # Extract current price
        extracted_price_ = float(div_.text)

    except Exception as exception_:
        __log_error(f'Error during requests to {url_}\n{type(exception_).__name__}\n{str(exception_)}')

    finally:
        driver.quit()

    return extracted_price_


# Internal method
def __log_error(exception_: str):
    """
    This function just prints exception, but you can make it do anything.

    :param exception_: to log
    """
    print(exception_)
    print('')


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a my_module.py file, when executed as the main program, the __name__ attribute will be '__main__',
# however if used by importing from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':

    # By default, scrape the IG Markets site
    # This is a static scraping that ignores JavaScript. It fetches web pages from the server without the help
    #   of a browser. You get exactly what you see in "view page source", and then you slice and dice it
    static_scrape_in_igmarkets_ = True

    # Also scrape Tradind View site, alternatively it could be set in False, to only scrape if fails scraping
    #   to IG Markets site (witch is the first scrape)
    # This is a dynamic scraping, it uses an actual browser (or a headless browser) and lets JavaScript do its thing.
    #   Then, it queries the DOM to extract the content it's looking for.
    dynamic_scrape_in_tradingview_ = True

    if static_scrape_in_igmarkets_:
        # We only fetches web pages from the server without the use of a browser.
        # URL to scrape https://www.ig.com/es/indices/mercado-indices/us-spx-500

        # Initialize params.
        # Base URL of IG Markets site as constant
        IG_BASE_URL = 'https://www.ig.com/es/indices/mercado-indices/'

        # You can change the index or stock for web scraping, but first you need to know which symbol to use
        symbol_ = 'us-spx-500'

        # Assemble the URL to scrape (request and parse)
        url_to_request_ = f'{IG_BASE_URL}{symbol_.lower()}'

        # Request page and extract current price with static scraping
        current_price_ = static_scraping(url_to_request_)

        if current_price_ > 0:
            # Show result
            print('\nUsing STATIC Web Scraping')
            print(f'Current price of {symbol_.upper()} CFD (by IG Markets) .: ${current_price_:.2f}')
        else:
            # Force dynamic scraping
            dynamic_scrape_in_tradingview_ = True

    if dynamic_scrape_in_tradingview_:
        # But, what happens if page content loads as a result of asynchronous JavaScript requests?
        #   We need use Dynamic Scraping.
        # URL to scrape: https://www.tradingview.com/symbols/FX-SPX500/

        # Initialize params
        # Base URL of Trading View site as constant
        TV_BASE_URL = 'https://www.tradingview.com/symbols/'

        # You can change the index or stock for web scraping, but first you need to know which symbol to use
        symbol_ = 'FX-SPX500'

        # Assemble the URL to scrape (request and parse)
        url_to_request_ = f'{TV_BASE_URL}{symbol_.upper()}'

        # Request page and extract current price with dynamic scraping
        current_price_ = dynamic_scraping(url_to_request_)

        if current_price_ > 0:
            # Show result
            print('\nUsing Dynamic Web Scraping')
            print(f'Current price of {symbol_.upper()}  CFD (by Trading View): ${current_price_:.2f}')
