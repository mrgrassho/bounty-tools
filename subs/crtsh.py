#!/usr/bin/env python3
from utils.common_crawler import CommonCrawler

URL = lambda t: f"https://crt.sh/?q={t}"
SELECTOR = 'body table td:nth-child(5)'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0'
}

def data(q):
    url = URL(q)
    cc = CommonCrawler(url, headers=HEADERS)
    return cc.response(SELECTOR)