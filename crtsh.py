#!/usr/bin/env python3
from sys import argv
from common_crawler import CommonCrawler

URL = lambda t: f"https://crt.sh/?q={t}"
SELECTOR = 'body table td:nth-child(5)'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0'
}

q = URL(argv[1])
cc = CommonCrawler(q, headers=HEADERS)
for d in cc.parse(SELECTOR):
    print(d)