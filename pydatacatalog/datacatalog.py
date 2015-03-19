#!/usr/bin/env python

import urllib2
import urllib
import json
import argparse

from datetime import date, datetime, timedelta
import time
import pytz
from pytz import timezone

import requests

args_conf = [
  { "name" : "symbol", "other" : {"help": "symbol to lookup"} },
  { "name" : "--host", "other" : { "help" : "host for datacatalog", "default" : "datacatalog01" }}
]

paris_zone = timezone('Europe/Paris')

def now_paris():
  return pytz.utc.localize(datetime.utcnow()).astimezone(paris_zone)

def deadline_passed(deadline) :
  return now_paris() > deadline

class DataCatalogError(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)

class DatacatalogDefaults(object):

  def __init__(self, host):
    self.host = host
  
  def latest(self, symbol):
    try:
      url = "http://{1}:3000/catalog/latest?{0}".format(urllib.urlencode({ "name": symbol }), self.host)
      resp = urllib2.urlopen(url)
      lines = resp.readlines()
      resp = json.loads(lines[0])
      if symbol in resp:
        return resp[symbol]["path"]
      else:
        raise DataCatalogError("Symbol {0} not in response: {1}".format(symbol, lines))
    except urllib2.URLError as e:
      raise DataCatalogError("Error accessing url : {0}. {1}".format(url, e.reason))

  def _available(self, symbols):
    resp = requests.get(url(self.host, symbols))
    return resp.status_code == 200


  def _unavailable(self, symbols):
    resp = requests.get(self.url(self.host, symbols))
    if resp.status_code == 404 :
      return json.loads(resp.content)
    else:
      return []

  def _url(self, symbols):
    symbols = "&".join(["name={0}".format(s) for s in symbols])
    url = "http://{host}:3000/catalog?from={today}&{symbols}".format(symbols=symbols, host=self.host, today=self._today())
    return url

  def _today(self):
    return datetime.date.today().strftime("%Y-%m-%d")

  def wait(self, symbols, deadline, waiting_time=600, deadline_passed = deadline_passed):
    def valid (tries):
      ok = len(symbols) == 0 or self._available(symbols)
      if not ok and not deadline_passed(deadline):
         print "Waiting for symbols: {0}".format(self._unavailable(symbols))
         time.sleep(waiting_time)
         return valid(tries + 1)
      else:
         return (ok,tries)
    return valid(1) 

  def wait_or_latest(self, symbols, deadline, waiting_time=600, deadline_passed = deadline_passed):
    " waits till symbols are resolved or the deadline and returns the latest path for the symbols"
    self.wait(symbols, deadline = deadline, waiting_time = waiting_time, deadline_passed = deadline_passed)
    list_symbols = [{symbol: self.latest(symbol)} for symbol in symbols]
    return reduce(lambda x,y: dict(x.items() + y.items()), list_symbols)


def parse_args(args_conf):
  parser = argparse.ArgumentParser()
  for arg in args_conf:
    parser.add_argument(arg["name"], **arg["other"])
  return parser.parse_args()

if __name__ == '__main__':
  args = parse_args(args_conf)
  datacat = DatacatalogDefaults(args.host)
  print datacat.latest(args.symbol)
