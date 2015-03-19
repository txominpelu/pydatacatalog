from pydatacatalog import datacatalog
import unittest

import time
from pytz import timezone
import pytz
from datetime import date, datetime, timedelta

def func_from_results(results):
  last = results[-1]
  for r in results:
    yield r
  while True:
    yield last

class DatacatalogTestDefaults(datacatalog.DatacatalogDefaults):

  def __init__(self, available, timeout, unavailable = lambda x: [], latest = lambda x: x):
    self.available = available
    self.timeout = timeout
    self.unavailable = unavailable
    self._latest = latest
  
  def latest(self, symbol):
    return self._latest(symbol)

  def _available(self, symbols):
    return self.available(symbols)

  def _unavailable(self, symbols):
    return self.unavailable(symbols)

  def wait_or_latest(self, symbols, deadline, waiting_time=600):
    return super(DatacatalogTestDefaults, self).wait_or_latest(symbols, deadline, waiting_time = waiting_time, deadline_passed = self.timeout)

  def wait(self, symbols, deadline, deadline_passed = lambda x: False, waiting_time=600):
    return super(DatacatalogTestDefaults, self).wait(symbols, deadline, waiting_time = waiting_time, deadline_passed = self.timeout)

class TestSequenceFunctions(unittest.TestCase):

  #def setUp(self):
  def test_wait(self):
    symbols = [ "s1", "s2", "s3" ]
    available = func_from_results([False])
    timeout = func_from_results([False, False, True])
    datacat = DatacatalogTestDefaults(available=lambda x: available.next(), timeout= lambda x: timeout.next())
    (ok, tries) = datacat.wait(symbols, waiting_time=1, deadline=datacatalog.now_paris())
    # make sure the shuffled sequence does not lose any elements
    self.assertEqual(ok,False)
    self.assertEqual(tries,3)

  def test_wait_or_latest(self):
    symbols = [ "s1", "s2", "s3" ]
    latest = func_from_results([ "s1.value", "s2.value", "s3.value" ])
    available = func_from_results([False])
    timeout = func_from_results([False, False, True])
    datacat = DatacatalogTestDefaults(available=lambda x: available.next(), timeout= lambda x: timeout.next(), latest = lambda x: latest.next())
    symbols = datacat.wait_or_latest(symbols, deadline=datacatalog.now_paris(), waiting_time=1)
    # make sure the shuffled sequence does not lose any elements
    self.assertEqual(symbols,{
      "s1": "s1.value",
      "s2": "s2.value",
      "s3": "s3.value"
     })

if __name__ == '__main__':
    unittest.main()


