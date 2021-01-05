#!/usr/bin/env python3

import unittest
import asstimeshift
from asstimeshift import Timestamp

class TestAss(unittest.TestCase):
    def test_from_timestamp(self):
        r = Timestamp('0:44:28.28')
        self.assertEqual(2668280, r.ts)

        r = Timestamp('0:00:00.00')
        self.assertEqual(0, r.ts)

        r = Timestamp('0:00:00')
        self.assertEqual(0, r.ts)

        r = Timestamp('0:00:01')
        self.assertEqual(1000, r.ts)

        # 支持以srt时间戳导入
        r = Timestamp('01:02:03,377')
        self.assertEqual(3723377, r.ts)

        # 支持以秒数导入
        r = Timestamp('1800')
        self.assertEqual(1800000, r.ts)

        r = Timestamp('1800.0')
        self.assertEqual(1800000, r.ts)

        # 检查精度
        r = Timestamp('0:05:42.16')
        self.assertEqual(342160, r.ts)

        r = Timestamp('0:0:0.1')
        self.assertEqual(100, r.ts)

        r = Timestamp('0:0:0.12')
        self.assertEqual(120, r.ts)

        r = Timestamp('0:0:0.123')
        self.assertEqual(123, r.ts)

        r = Timestamp('0:0:0.1234')
        self.assertEqual(123, r.ts)

        r = Timestamp('0:0:0.12345')
        self.assertEqual(123, r.ts)

        r = Timestamp('0:0:0.123456')
        self.assertEqual(123, r.ts)

    def test_to_timestamp(self):
        r = Timestamp(2668280)
        self.assertEqual(str(r), '0:44:28.28')

        r = Timestamp(0)
        self.assertEqual(str(r), '0:00:00.00')

        r = Timestamp((11*3600+11*60+11.11)*1000)
        self.assertEqual(str(r), '11:11:11.11')

        r = Timestamp('0:05:42.16')
        self.assertEqual(str(r), '0:05:42.16')

        r = Timestamp(99999)
        self.assertEqual(str(r), '0:01:40.00')

        r = Timestamp(99995)
        self.assertEqual(str(r), '0:01:40.00')

        r = Timestamp(99994)
        self.assertEqual(str(r), '0:01:39.99')

        r = Timestamp(100005)
        self.assertEqual(str(r), '0:01:40.00')

        r = Timestamp(100006)
        self.assertEqual(str(r), '0:01:40.01')

        with self.assertRaises(RuntimeError):
            r = Timestamp()
            r.ts = -1
            str(r)

    def test_calc_correction(self):
        f1 = Timestamp('0:00:00.00')
        f2 = Timestamp('1:00:00.00')
        t1 = Timestamp('0:00:00.00')
        t2 = Timestamp('0:30:00.00')
        k, b = asstimeshift.calc_correction(t1, t2, f1, f2)
        self.assertEqual(k, 0.5)
        self.assertEqual(b, 30*60*1000-3600*1000/2)

    def test_correct_time(self):
        bad_timestamp = Timestamp('1:00:00.00')
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
