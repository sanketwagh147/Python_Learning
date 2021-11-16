from add1 import addition
import unittest

class SimpleTest(unittest.TestCase):
    def test_addition(self):
        a_l = [1,2,3,4,5,6]
        b_l = [1,2,3,4,5,6]
        res = [2,4,6,9,10,12]
        for i in range(len(a_l)):
            self.assertEqual(addition(a_l[i],b_l[i]),res[i])

if __name__ == '__main__':
    unittest.main()

