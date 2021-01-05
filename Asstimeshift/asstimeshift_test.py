#!/usr/bin/env python3

import unittest
import asstimeshift

class TestAss(unittest.TestCase):
    def test_from_timestamp(self):
        r = asstimeshift.Timestamp('0:44:28.28')
        self.assertEqual(2668280, r.ts)

        r = asstimeshift.Timestamp('0:00:00.00')
        self.assertEqual(0, r.ts)

        r = asstimeshift.Timestamp('0:00:00')
        self.assertEqual(0, r.ts)

        # 支持以srt时间戳导入
        r = asstimeshift.Timestamp('01:02:03,377')
        self.assertEqual(3723377, r.ts)

    def test_to_timestamp(self):
        r = asstimeshift.Timestamp()
        r.ts = 2668280
        self.assertEqual(str(r), '0:44:28.28')

        r = asstimeshift.Timestamp()
        r.ts = 0
        self.assertEqual(str(r), '0:00:00.00')

        r = asstimeshift.Timestamp()
        r.ts = (11*3600+11*60+11.11)*1000
        self.assertEqual(str(r), '11:11:11.11')

        with self.assertRaises(RuntimeError):
            r = asstimeshift.Timestamp()
            r.ts = -1
            str(r)

    def test_calc_correction(self):
        f1 = asstimeshift.Timestamp('0:00:00.00')
        f2 = asstimeshift.Timestamp('1:00:00.00')
        t1 = asstimeshift.Timestamp('0:00:00.00')
        t2 = asstimeshift.Timestamp('0:30:00.00')
        k, b = asstimeshift.calc_correction(t1, t2, f1, f2)
        self.assertEqual(k, 0.5)
        self.assertEqual(b, 30*60*1000-3600*1000/2)

    def test_correct_time(self):
        bad_timestamp = asstimeshift.Timestamp('1:00:00.00')
        k = 0.5
        b = 3600 * 1000
        r = bad_timestamp.correct(k, b)
        self.assertEqual(str(r), '1:30:00.00')

    def test_if_ass_timestamp_line(self):
        r = asstimeshift.if_ass_timestamp_line(r'Dialogue: 0,0:43:06.32,0:43:07.45,*Default,,0,0,0,,政府在干吗 \N{\fn微软雅黑}{\fs14}나라에서 뭐 하는 거야?')
        self.assertNotEqual(r, None)

        r = asstimeshift.if_ass_timestamp_line(r'Dialogue: 00:43:06.32,0:43:07.45,*Default,,0,0,0,,政府在干吗 \N{\fn微软雅黑}{\fs14}나라에서 뭐 하는 거야?')
        self.assertEqual(r, None)

        r = asstimeshift.if_ass_timestamp_line(r'Dialogue: 0,0:43:06,0:43:07,*Default,,0,0,0,,政府在干吗 \N{\fn微软雅黑}{\fs14}나라에서 뭐 하는 거야?')
        self.assertNotEqual(r, None)
        self.assertEqual(r.group(1), '0:43:06')
        self.assertEqual(r.group(2), '0:43:07')

if __name__ == '__main__':
    unittest.main()

# vim: set sw=4 tabstop=4 expandtab :
