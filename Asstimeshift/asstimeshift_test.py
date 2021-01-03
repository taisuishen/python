import unittest
import asstimeshift

class TestAss(unittest.TestCase):
    def test_from_timestamp(self):
        r = asstimeshift.from_timestamp('0:44:28.28')
        self.assertEqual(2668280, r)
        
    def test_to_timestamp(self):
        r = asstimeshift.to_timestamp(2668280)
        self.assertEqual(r, '0:44:28.28')  

if __name__ == '__main__':
    unittest.main()