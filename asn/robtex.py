#!/usr/bin/env python3
from sys import argv
from common_crawler import CommonCrawler
from json import loads

# Given an ASN Number it lookup for Network Ranges
URL = lambda q: f"https://freeapi.robtex.com/asquery/{q}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0'
}

q = URL(argv[1])
cc = CommonCrawler(q, headers=HEADERS)
urls = loads(cc.response())
for e in urls['nets']:
    print(e['n'])