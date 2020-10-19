#!/usr/bin/env python3
from urllib.request import Request, urlopen, HTTPCookieProcessor
from bs4 import BeautifulSoup
from sys import argv
from http.cookiejar import CookieJar
import requests


q = argv[1]
target = f"https://searchdns.netcraft.com/?restriction=site+contains&host={q}&position=limited"
cookies = {'required_cookie': 'netcraft_js_verification_challenge=djF8d1VtNXYzWTRqSStQS05PL3VHMTdxUDJQSVFEVUZOT2NrVkowZW82dEJJcUhJd3o3bGx1Nzhh%0ATS9jR2hmSldTd0dkWVd6UDVpS0NZSgpBeHhEYWtxOCtnPT0KfDE2MDMxMTkwNjM%3D%0A%7C95c5ecf846f28acbf5c2112f7b0517674e137ea3; netcraft_js_verification_response=f2cbe75ac6596d068cb95adcf3dc07ba3684430a'}
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(target, cookies=None, headers=headers)
webpage = response.text

print(webpage)



