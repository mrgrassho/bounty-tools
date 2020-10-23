#!/usr/bin/env python3
from requests import request
from bs4 import BeautifulSoup
from http.client import HTTPException

HEADERS = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "en-US,en;q=0.5",
    'accept-encoding': "gzip, deflate",
    'connection': "close",
    'upgrade-insecure-requests': "1",
    'cache-control': "no-cache"
}

class CommonCrawler(object):
    """
    A class to Crawl an HTTP Resource.

    ...

    Attributes
    ----------
    url : str
        Target URL of the HTTP Request
    header : dict, optional
        HTTP Headers

    Methods
    -------
    request(method=""):
        Make a HTTP Request.
    
    response(selector=""):
        Extracts data from HTTP Response using selector if present, 
        otherwise returns the entire document
    """


    def __init__(self, url, headers=HEADERS):
        """
        Constructs all the necessary attributes for the CommonCrawler object.

        Parameters
        ----------
            url : str
                Target URL of the HTTP Request
            header : dict, optional
                HTTP Headers
        """
        self.url = url
        self.headers = headers
        self._response = self.request()


    def request(self, method="GET"):
        """
        Make a HTTP Request.

        Parameters
        ----------
        method : str, optional
            HTTP Method, default: GET

        Returns
        -------
        `bs4.BeautifulSoup` object
        """
        try:
            response = request(method, self.url, headers=self.headers)
            return BeautifulSoup(response.text, "html.parser")
        except HTTPException as e:
            return(e)
        
    
    def response(self, selector=None):
        """
        Extracts data from HTTP Response using selector if present, 
        otherwise returns the entire document
 
        Attributes
        ----------
        selector : str, optional
            CSS Selector, behaves like querySelectorAll() in JS

        Returns
        -------
        str
        """
        if (selector):
            elements = self._response.select(selector)
            return set(sorted(set([e.text.lower() for e in elements])))
        else:
            return self._response.text