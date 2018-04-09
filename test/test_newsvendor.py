import sys
sys.path.append('../src')

import unittest
from newsvendor import Newsvendor
import scipy.stats as stats

class TestNewsvendor(unittest.TestCase):

    def test_init(self):
        newsvendor = Newsvendor(price=150, cost=100, salvage_value=70, quantity_start=1)
        self.assertEqual(newsvendor.price, 150)
        self.assertEqual(newsvendor.cost, 100)
        self.assertEqual(newsvendor.salvage_value, 70)
        self.assertEqual(newsvendor.quantity_start, 1)
        self.assertEqual(newsvendor.underage_cost, 50)
        self.assertEqual(newsvendor.overage_cost, 30)
        

if __name__ == '__main__':
    unittest.main()