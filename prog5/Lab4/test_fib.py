import unittest
from gen_fib import fib



class TestFib(unittest.TestCase):
    def setUp(self):
        self.fib = fib

    def test_fib_1(self):
        self.assertEqual(self.fib(3), [0, 1, 1])
    
    def test_fib_2(self):
        self.assertEqual(self.fib(5), [0, 1, 1, 2, 3])

    def test_fib_3(self):
        self.assertEqual(self.fib(0), [])

    def test_fib_4(self):
        self.assertEqual(self.fib(-1), [])

unittest.main()