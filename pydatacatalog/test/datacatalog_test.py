from pydatacatalog import datacatalog
import unittest


def func_from_results(results):
  last = results[-1]
  for r in results:
    yield r
  while True:
    yield last

class TestSequenceFunctions(unittest.TestCase):

  #def setUp(self):
  def test_wait(self):
    symbols = [ "s1", "s2", "s3" ]
    available = func_from_results([False])
    timeout = func_from_results([False, False, True])
    (ok, tries) = datacatalog.wait(symbols, timeout=timeout.next, available=lambda x: available.next(), waiting_time=1, host="localhost", unavailable = lambda x, y: [])
    # make sure the shuffled sequence does not lose any elements
    self.assertEqual(ok,False)
    self.assertEqual(tries,3)

  def test_wait_or_latest(self):
    symbols = [ "s1", "s2", "s3" ]
    latest = func_from_results([ "s1.value", "s2.value", "s3.value" ])
    available = func_from_results([False])
    timeout = func_from_results([False, False, True])
    symbols = datacatalog.wait_or_latest(symbols, latest=lambda x: latest.next(), timeout=timeout.next, available=lambda x: available.next(), waiting_time=1, host="localhost", unavailable = lambda x, y: [])
    # make sure the shuffled sequence does not lose any elements
    self.assertEqual(symbols,{
      "s1": "s1.value",
      "s2": "s2.value",
      "s3": "s3.value"
     })

if __name__ == '__main__':
    unittest.main()


