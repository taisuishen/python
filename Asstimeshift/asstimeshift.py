#!/usr/bin/env python3

import argparse, re, sys

try:
    from functools import lru_cache
    from chardet import detect as _chardet_detect
    _chardet_detect = lru_cache(_chardet_detect)
except ImportError:
    _chardet_detect = None

def chardet_detect(bytes):
    encoding = 'GBK'
    if _chardet_detect is None:
        return encoding
    else:
        r = _chardet_detect(bytes)

    if r:
        encoding = r['encoding']
        if encoding == 'GB2312':
            encoding = 'GBK'

    return encoding

class Timestamp():
    @staticmethod
    def from_timestamp(str_):
        "时间戳转换为毫秒"
        l = str_.split(":")
        if len(l) != 3:
            try:
                v = float(str_)
            except TypeError as e:
                raise RuntimeError("错误的时间戳")
            return int(v * 1000)

        if ',' in l[2]:
            l[2] = l[2].replace(',', '.')

        hours, minutes = int(l[0]), int(l[1])

        dotp = l[2].find('.')
        if dotp >= 0:
            seconds = int(l[2][0:dotp])
            r = int((hours*3600 + minutes*60 + seconds) * 1000)
            ms = l[2][dotp+1:dotp+1+3]
            if len(ms) == 1:
                ms = int(ms) * 100
            elif len(ms) == 2:
                # ASS: 两位小数
                ms = int(ms) * 10
            else:
                # SRT: 三位小数
                ms = int(ms)
            return r + ms

        seconds = int(l[2])
        return int((hours*3600 + minutes*60 + seconds) * 1000)

    @staticmethod
    def to_timestamp(sec):
        "毫秒转换时间戳"
        if sec < 0:
            raise RuntimeError("错误的时间戳: {}".format(sec))

        hours, r = divmod(sec, 3600000)
        minutes, r = divmod(r, 60000)
        seconds, r = divmod(r, 1000)
        r = round(r / 10)
        if r >= 100:
            seconds += 1
            r -= 100

        return "%d:%02d:%02d.%02d" % (hours, minutes, seconds, r)

    def __init__(self, str_=None):
        self.ts = 0
        if isinstance(str_, str):
            self.ts = self.from_timestamp(str_)
        elif str_ is not None:
            self.ts = int(str_)

    def correct(self, k, b):
        "返回修正的时间戳对象"
        n = Timestamp()
        n.ts = int(self.ts * k + b)

        return n

    def __str__(self):
        return self.to_timestamp(self.ts)

    def __sub__(self, o):
        n = Timestamp()
        n.ts = self.ts - o.ts
        return n

    def __truediv__(self, o):
        return self.ts / o.ts

def parse_args():
    "处理命令行输入参数"
    parser = argparse.ArgumentParser(description="字幕调整时间轴")
    parser.add_argument("-i", "--input", help="输入字幕文件名")
    parser.add_argument("-o", "--output", help="输出字幕文件名")
    parser.add_argument("--f1", help="原始字幕起始时间", type=Timestamp)
    parser.add_argument("--f2", help="原始字幕结束时间", type=Timestamp)
    parser.add_argument("--t1", help="目标字幕起始时间", type=Timestamp)
    parser.add_argument("--t2", help="目标字幕结束时间", type=Timestamp)

    return parser

def calc_correction(t1, t2, f1, f2):
    k = (t2 - t1) / (f2 - f1)
    b = t2.ts - k * f2.ts
    return k, b

TIMESTAMP_TS = r'([0-9]+:[0-9]+:[0-9]+(?:\.[0-9]+)?)'
TIMESTAMP_TS_RE = re.compile(TIMESTAMP_TS)
TIMESTAMP_LINE_RE = re.compile(r'^Dialogue: [0-9]+,\s*'+TIMESTAMP_TS+',\s*'+TIMESTAMP_TS+',\s*')

def if_ass_timestamp_line(line):
    m = TIMESTAMP_LINE_RE.match(line)
    return m

def replace_ass_timestamp_line(line, nts1, nts2):
    l = [ nts1, nts2 ]
    it = iter(l)
    line = re.sub(TIMESTAMP_TS_RE, lambda x: next(it), line)
    return line

FILTER_ASS_LINE_RE = re.compile(r'\{.*?\}')
def filter_ass_line(line):
    pos = line.rfind(',,')
    if pos >= 0:
        line = line[pos+2:]
    return re.sub(FILTER_ASS_LINE_RE, '', line).replace(r'\N', '')

def get_all_lines(args):
    def parse():
        for line in fi:
            line = line.rstrip()
            m = if_ass_timestamp_line(line)
            if m:
                d[m.group(1)] = filter_ass_line(line)

    d = {}

    try:
        with open(args.input, "r", encoding='utf-8') as fi:
            parse()
    except UnicodeDecodeError:
        d = {}
        with open(args.input, "rb") as fi:
            b = fi.read()
        with open(args.input, "r", encoding=chardet_detect(b)) as fi:
            parse()

    return d

def asstimeshift(args, fi, fo):
    warns = []
    k, b = calc_correction(args.t1, args.t2, args.f1, args.f2)
    for line in fi:
        line = line.rstrip()
        # print (line)
        m = if_ass_timestamp_line(line)

        if m:
            d1 = Timestamp(m.group(1))
            d2 = Timestamp(m.group(2))

            nd1 = d1.correct(k, b)
            nd2 = d2.correct(k, b)

            if nd1.ts < 0 or nd2.ts < 0:
                warn_msg = "警告: 时间戳为负数，已被忽略: {}".format(line)
                print(warn_msg, file=sys.stderr)
                warns.append(warn_msg)
                continue

            line = replace_ass_timestamp_line(line, str(nd1), str(nd2))

        fo.write(line + "\n")

    return warns

def main():
    parser = parse_args()
    args = parser.parse_args()

    if args.t1 == None or \
       args.t2 == None or \
       args.f1 == None or \
       args.f2 == None:
        print ("{}: 请输入字幕开始结束时间\n".format(parser.prog), file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if args.input == None or args.output == None:
        print ("{}: 请输入和输出字幕文件名\n".format(parser.prog), file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    try:
        with open(args.output, "w", encoding='utf-8') as fo:
            with open(args.input, "r", encoding='utf-8') as fi:
                asstimeshift(args, fi, fo)
    except UnicodeDecodeError:
        with open(args.input, "rb") as fi:
            b = fi.read()
        with open(args.output, "w", encoding='utf-8') as fo:
            with open(args.input, "r", encoding=chardet_detect(b)) as fi:
                asstimeshift(args, fi, fo)

if __name__ == "__main__":
    main()

# vim: set sw=4 tabstop=4 expandtab :
