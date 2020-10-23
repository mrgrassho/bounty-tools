#!/usr/bin/env python3
from utils.common_crawler import CommonCrawler


URL = lambda t: f"http://archive.is/%2A.{t}"
SELECTOR = '#CONTENT .TEXT-BLOCK a'
HEADERS = {
    'host': "archive.is",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "en-US,en;q=0.5",
    'accept-encoding': "gzip, deflate",
    'referer': "http://archive.is/offset=100/*.microsoft.com",
    'connection': "close",
    'upgrade-insecure-requests': "1",
    'cache-control': "no-cache"
}

def data(q):
    url = URL(q)
    cc = CommonCrawler(url, headers=HEADERS)
    return cc.response(SELECTOR)