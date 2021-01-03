import argparse, re

class Timestamp():
    @staticmethod
    def from_timestamp(str):
        "时间戳转换为毫秒"
        l = str.split(":")
        if len(l) != 3:
            raise RuntimeError("错误的时间戳")
        hours, minutes , seconds = int(l[0]), int(l[1]), float(l[2])

        return (hours*3600 + minutes*60 + seconds) * 1000

    @staticmethod    
    def to_timestamp(sec):
        "毫秒转换时间戳"
        if sec < 0:
            raise RuntimeError("错误的时间戳: {}".format(sec))
        
        hours, r = divmod(sec, 3600000)
        minutes, r = divmod(r, 60000)
        seconds, r = divmod(r, 1000)
        r = r // 10

        return "%d:%02d:%02d.%02d" % (hours, minutes, seconds, r)
        
    def __init__(self, str=None):
        self.ts = 0
        if str:
            self.ts = self.from_timestamp(str)
        
    def correct(self, k, b):
        "返回修正的时间戳对象"
        n = Timestamp()
        n.ts = self.ts * k + b

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
    parser = argparse.ArgumentParser("字幕调整时间轴")
    parser.add_argument("-i", "--input", help="输入字幕文件名")
    parser.add_argument("-o", "--output", help="输出字幕文件名")
    parser.add_argument("--f1", help="原始字幕起始时间", type=Timestamp)
    parser.add_argument("--f2", help="原始字幕结束时间", type=Timestamp)
    parser.add_argument("--t1", help="目标字幕起始时间", type=Timestamp)
    parser.add_argument("--t2", help="目标字幕结束时间", type=Timestamp)

    return parser.parse_args()

def calc_correction(t1, t2, f1, f2):
    k = (t1 - t2) / (f1 - f2)
    b = t2.ts - k * f2.ts
    return k, b

TIMESTAMP_LINE_RE = re.compile(r'^Dialogue: [0-9]+,([0-9]+:[0-9]+:[0-9]+(?:\.[0-9]+)?),([0-9]+:[0-9]+:[0-9]+(?:\.[0-9]+)?),')
def if_ass_timestamp_line(line):
    m = TIMESTAMP_LINE_RE.match(line)
    return m
    
def asstimeshift(args, fi, fo):
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
            
            line = line.replace(m.group(1), str(nd1), 1)
            line = line.replace(m.group(2), str(nd2), 1)

        fo.write(line + "\n")

def main():
    args = parse_args()

    if args.t1 == None or \
       args.t2 == None or \
       args.f1 == None or \
       args.f2 == None:
        raise RuntimeError("请输入字幕开始结束时间")

    if args.input == None or args.output == None:
        raise RuntimeError("请输入和输出字幕文件名")

    with open(args.output, "w", encoding='utf-8') as fo:
        with open(args.input, "r", encoding='utf-8') as fi:
            asstimeshift(args, fi, fo)

if __name__ == "__main__":
    main()
