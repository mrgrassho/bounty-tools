#!/usr/bin/env python3
from urllib.request import Request, urlopen, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from sys import argv

q = argv[1]
target = f"https://bgp.he.net/search?search%5Bsearch%5D={q}&commit=Search"
req = Request(target, headers={
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Host':'bgp.he.net',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'close',
    'Referer':'https://bgp.he.net/',
    'Cookie':'c=BAgiEjIwMS4yNTUuOC4xNTg%3D--99da60b8697980295a552ef5d5a4aaeb7a2da9b8; _bgp_session=jj; __utmt=1',
    'Upgrade-Insecure-Requests':'1'
})
response = urlopen(req, timeout=30)
str(response.headers)
import pdb; pdb.set_trace()
content = response.read()
data = BeautifulSoup(content, "html.parser")
print(data)
urls = data.select('div#search tr')
import pdb; pdb.set_trace()
# a = []
# for url in urls: 
#     a += str(url).strip("<td>").strip("</td>").split('<br/>')
# for s in set(a):
#     print(s)



