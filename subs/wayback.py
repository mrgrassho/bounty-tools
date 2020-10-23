#!/usr/bin/env python3
from utils.common_crawler import CommonCrawler
from json import loads, dump
from re import findall

URL = lambda t: f"http://web.archive.org/cdx/search/cdx?url=*.{t}/*&output=json&fl=original&collapse=urlkey"
# HEADERS = {
#     'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
# }

def data(q):
    url = URL(q)
    q.replace(".", "\.")
    sub_url = f"(?:http[s]?://)([\w\d\-\.\~]*\.{q}).*"
    cc = CommonCrawler(url)
    urls = []
    for row in cc.response():
        try:
            urls += loads(row)
        except Exception as e:
            pass
    subs = set() 
    for url in urls:
        sub = findall(sub_url, url[0])
        if (sub):
            subs.add(sub[0])
    return subs