import unittest
import asstimeshift

class TestAss(unittest.TestCase):
    def test_from_timestamp(self):
        r = asstimeshift.from_timestamp('0:44:28.28')
        self.assertEqual(2668280, r)
        
        r = asstimeshift.from_timestamp('0:00:00.00')
        self.assertEqual(0, r)
        
        r = asstimeshift.from_timestamp('0:00:00')
        self.assertEqual(0, r)
        
    def test_to_timestamp(self):
        r = asstimeshift.to_timestamp(2668280)
        self.assertEqual(r, '0:44:28.28')

        r = asstimeshift.to_timestamp(0)
        self.assertEqual(r, '0:00:00.00')
        
        r = asstimeshift.to_timestamp((11*3600+11*60+11.11)*1000)
        self.assertEqual(r, '11:11:11.11')
        
        with self.assertRaises(RuntimeError):
            r = asstimeshift.to_timestamp(-1)

    def test_calc_correction(self):
        f1 = asstimeshift.from_timestamp('0:00:00.00')
        f2 = asstimeshift.from_timestamp('1:00:00.00')
        t1 = asstimeshift.from_timestamp('0:00:00.00')
        t2 = asstimeshift.from_timestamp('0:30:00.00')
        k, b = asstimeshift.calc_correction(t1, t2, f1, f2)
        self.assertEqual(k, 0.5)
        self.assertEqual(b, 30*60*1000-3600*1000/2)
    
    def test_correct_time(self):
        bad_timestamp = asstimeshift.from_timestamp('1:00:00.00')
        k = 0.5
        b = 3600 * 1000
        r = asstimeshift.correct_time(bad_timestamp, k, b)
        self.assertEqual(r, asstimeshift.from_timestamp('1:30:00.00'))

if __name__ == '__main__':
    unittest.main()