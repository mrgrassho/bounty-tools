
from requests import request
from sys import argv
from json import loads

q = argv[1]
# Given an ASN Number it lookup for Network Ranges
url = f"https://freeapi.robtex.com/asquery/{q}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0'
}
response = request("GET", url, headers=headers)
urls = loads(response.text)
for e in urls['nets']:
    print(e['n'])