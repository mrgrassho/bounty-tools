#!/usr/bin/env python3
from requests import get
from sys import argv

q = argv[1]
target = f"https://censys.io/certificates?q={q}"
headers = {'User-Agent': 'Mozilla/5.0'}
response = get(target, headers=headers)
print(response.text)



