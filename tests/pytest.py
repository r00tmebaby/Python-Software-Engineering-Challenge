import unittest
from models import database

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([3, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((4, 2)), 6, "Should be 6")



if __name__ == '__main__':
    unittest.main()