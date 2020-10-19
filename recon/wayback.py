from requests import request
from sys import argv
from json import loads
from re import findall

q = argv[1]
url = f"http://web.archive.org/cdx/search/cdx?url=*.{q}/*&output=json&fl=original&collapse=urlkey"
q = q.replace(".", "\.")
SUB_URL = f"(?:http[s]?://)(.*\.{q})"
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}
response = request("GET", url, headers=headers)
urls = loads(response.text)
subs = set() 
for url in urls:
    sub = findall(SUB_URL, url[0])
    if (sub):
        subs.add(sub[0])
for sub in subs:    
    print(sub)
