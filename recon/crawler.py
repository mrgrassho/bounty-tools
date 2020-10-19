#!/usr/bin/env python3
from bs4 import BeautifulSoup
from re import match, findall, split
from graphviz import Digraph
from datetime import datetime
from os.path import join, exists
from os import mkdir
from itertools import cycle
import networkx as nx
import numpy as np
import asyncio
from time import time, sleep
import aiohttp
from sys import stdout
from threading import Thread
import argparse

URL_RE = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
DOMAIN_RE = '(?:https:\/\/|http:\/\/){0,1}[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9]+(?:\-[a-zA-Z0-9]+){0,1})+'

# To rewrite this use --always-graph
MAX_NODES = 300

class bcolors:
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'


class Crawler(object):
   
   def __init__(self, target, verbose=True, depth=10, save_html=False, timeout=20, parallel_requests=20, always_graph=False):
      if (not target.startswith(("https://", "http://"))):
         target = "http://" + target
      self._target = target
      self._verbose = verbose
      self._domain_no_http = split("https://|http://", target)[1].split("/")[0]
      self._domain = findall(DOMAIN_RE, self._target)[0]
      self._depth = depth
      self._save_html = save_html
      self._timeout = timeout
      self._parallel_requests = parallel_requests
      self._always_graph = always_graph
      self._out = self._domain_no_http + "-" + self.now()
      if (not exists(self._out) and self._save_html):
         mkdir(self._out)


   def get_links(self, soup, target):
      if (soup is None):
         return []
      links = set()
      cnt = 0
      for link in soup.findAll('a'):
         url = link.get('href')
         if (url != None and url != ''):
            r = match(URL_RE, url)
            if (r):
               match_url = r.group()
               if (not match_url.startswith(("https://", "http://"))):
                  match_url = self._domain + "/" + match_url
               links.add(match_url)
               cnt += 1
      return list(links)


   async def fetch(self, session, url):
      try:
         async with session.get(url) as response:
            html = await response.text()
            if (self._verbose):
               if (response.status >= 200 and response.status < 300):
                  print(f" {bcolors.OKGREEN}[+]{bcolors.ENDC} {url}{bcolors.OKGREEN} ({response.status} {response.reason}) {bcolors.ENDC}")
               elif (response.status >= 300 and response.status < 400):
                  print(f" {bcolors.WARNING}[!]{bcolors.ENDC} {url}{bcolors.WARNING} ({response.status} {response.reason}) {bcolors.ENDC}")
               elif (response.status >= 400):
                  print(f" {bcolors.FAIL}[-]{bcolors.ENDC} {url}{bcolors.FAIL} ({response.status} {response.reason}) {bcolors.ENDC}")
            return BeautifulSoup(html, "html.parser")
      except Exception as e:
         if (self._verbose):
            print(f" {bcolors.FAIL}[!] Could not download {url} – ERROR: {e} {bcolors.ENDC}")
         return None


   def now(self):
      return datetime.isoformat(datetime.now()).split('.')[0].replace(":", ";")


   def generate_graph(self, graph_data):
      dot = Digraph(comment=f'Crawling {self._target}')
      # Add nodes
      for k in graph_data:
         dot.node(graph_data[k]['id'], k)
      # Add edges
      for k in graph_data:
         for edge in graph_data[k]['edges']:
            dot.edge(graph_data[k]['id'], edge)
      dot.render(join(f'graph-{self.now()}-{self._depth}', f'{self._domain_no_http}.gv'), format='png') 


   async def save_html(self, target, data):
      if (self._save_html):
         with open(join(self._out, split("https://|http://", target)[1].replace("/",'$') + '.html'), 'w') as f:
            f.writelines(str(data))


   async def extract_data(self, todo_link, graph_data, todo):
      timeout = aiohttp.ClientTimeout(total=self._timeout)
      async with aiohttp.ClientSession(timeout=timeout) as session:
         page = await self.fetch(session, todo_link)
         if (page is None):
            return None
         await self.save_html(todo_link,page)
         links = self.get_links(page, todo_link)
         for link in links:
            if (link in graph_data):
               graph_data[todo_link]['edges'].append(graph_data[link]['id'])
            else:
               if (len(graph_data) < self._depth):
                  newid = f'{len(graph_data)}'
                  graph_data[link] = {'id': newid, 'edges': []}
                  graph_data[todo_link]['edges'].append(newid)
                  todo.append(link)
               else:
                  return None


   def process(self):
      start = time()
      if (self._target is None):
         raise Exception("Target MUST be specified.")
      todo = [self._target]
      graph_data = dict()
      graph_data[self._target] = {'id':'0', 'edges': []}
      while len(todo) != 0:
         newtodo = []
         loop = asyncio.get_event_loop()
         f = asyncio.wait([self.extract_data(td, graph_data, newtodo) for td in todo[:self._parallel_requests]])
         loop.run_until_complete(f)
         todo = todo[self._parallel_requests:] + newtodo
      print(f" {bcolors.OKGREEN}[+] Crawl Time: {bcolors.ENDC}{time() - start} ")
      print(f" {bcolors.OKGREEN}[+] Pages fetched: {bcolors.ENDC}{len(graph_data)} ")
      if (len(graph_data) > 1 and len(graph_data) < MAX_NODES) or (len(graph_data) > 1 and self._always_graph):
         self.start_loading("Graph", self.generate_graph, graph_data)


   def start_loading(self, phrase, func, f):
      self._done_task = False
      t = Thread(target=self.animate, args=[phrase])
      t.start()
      if (f == None):
         r = func()
      else:
         r = func(f)
      self._done_task = True
      return r


   def animate(self, phrase="", file=stdout):
      for c in cycle(['.  ', '.. ', '...']):
         if self._done_task:
            break
         file.write("\r " + bcolors.OKGREEN + "[+] Processing " +  phrase + c)
         file.flush()
         sleep(1)
      file.write("\r"+ bcolors.OKGREEN +" [+] "+  phrase +" done. " + " "*40 + bcolors.ENDC + "\n") 


def main():
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('target', type=str, help="Specify target URL")
   parser.add_argument('-d', '--depth', type=int, default=10, help="Specify number of pages to crawl")
   parser.add_argument('-s', '--save-html', action='store_true', default=False, help="Save fetched pages (HTML format)")
   parser.add_argument('-t', '--timeout', type=int, default=20, help="Specify HTTP Timeout (in seconds)")
   parser.add_argument('-p', '--parallel', type=int, default=20, help="Specify number of Parallel HTTP requests")
   # parser.add_argument('-v', '--verbose', action='store_true', default=False, help="Show no messages during process")
   parser.add_argument('-ag', '--always-graph', action='store_true', default=False, help="Generate GraphViz")
   args = parser.parse_args()
   c = Crawler(args.target, depth=args.depth, save_html=args.save_html, timeout=args.timeout, parallel_requests=args.parallel, always_graph=args.always_graph)
   c.process()

if __name__ == '__main__':
   main()