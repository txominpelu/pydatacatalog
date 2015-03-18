#!/usr/bin/env python

import urllib2
import urllib
import json
import argparse

import datetime
import time
import pytz

import requests

args_conf = [
  { "name" : "symbol", "other" : {"help": "symbol to lookup"} },
  { "name" : "--host", "other" : { "help" : "host for datacatalog", "default" : "datacatalog01" }}
]


class DataCatalogError(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)

def latest(host, symbol):
  try:
    url = "http://{1}:3000/catalog/latest?{0}".format(urllib.urlencode({ "name": symbol }), host)
    resp = urllib2.urlopen(url)
    lines = resp.readlines()
    resp = json.loads(lines[0])
    if symbol in resp:
      return resp[symbol]["path"]
    else:
      raise DataCatalogError("Symbol {0} not in response: {1}".format(symbol, lines))
  except urllib2.URLError as e:
    raise DataCatalogError("Error accessing url : {0}. {1}".format(url, e.reason))

def today():
  return datetime.date.today().strftime("%Y-%m-%d")

def url(host, symbols):
  symbols = "&".join(["name={0}".format(s) for s in symbols])
  url = "http://{host}:3000/catalog?from={today}&{symbols}".format(symbols=symbols, host=host, today=today())
  return url

def are_available(host, symbols):
  resp = requests.get(url(host, symbols))
  return resp.status_code == 200

def unavailable(host, symbols):
  resp = requests.get(url(host, symbols))
  if resp.status_code == 404 :
    return json.loads(resp.content)
  else:
    return []



def deadline_passed(deadline,current_time_paris) :
  return current_time_paris() > deadline

def wait(symbols, available, timeout, host, waiting_time=600, unavailable = unavailable):
  def valid (tries):
    ok = len(symbols) == 0 or available(symbols)
    if not ok and not timeout():
       print "Waiting for symbols: {0}".format(unavailable(host, symbols))
       time.sleep(waiting_time)
       return valid(tries + 1)
    else:
       return (ok,tries)
  return valid(1) 

def wait_or_latest(symbols, latest, available, timeout, host, waiting_time=600, unavailable = unavailable):
  " waits till symbols are resolved or the deadline and returns the latest path for the symbols"
  wait(symbols, available, timeout, host, waiting_time, unavailable)
  list_symbols = [{symbol: latest(symbol)} for symbol in symbols]
  return reduce(lambda x,y: dict(x.items() + y.items()), list_symbols)


def notify(start,end, symbol, path, host="localhost"):
  req = urllib2.Request("http://{0}:3000/catalog".format(host), "start={0}&end={1}&name={2}&path={3}".format(start, end, symbol, path))
  return urllib2.urlopen(req).getcode()

def parse_args(args_conf):
  parser = argparse.ArgumentParser()
  for arg in args_conf:
    parser.add_argument(arg["name"], **arg["other"])
  return parser.parse_args()

if __name__ == '__main__':
  args = parse_args(args_conf)
  print latest(args.symbol, args.host)
