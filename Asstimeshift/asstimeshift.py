import argparse, re

def parse_args():
    "处理命令行输入参数"
    parser = argparse.ArgumentParser("字幕调整时间轴")
    parser.add_argument("-i", "--input", help="输入字幕文件名")
    parser.add_argument("-o", "--output", help="输出字幕文件名")
    parser.add_argument("--f1", help="原始字幕起始时间", type=from_timestamp)
    parser.add_argument("--f2", help="原始字幕结束时间", type=from_timestamp)
    parser.add_argument("--t1", help="目标字幕起始时间", type=from_timestamp)
    parser.add_argument("--t2", help="目标字幕结束时间", type=from_timestamp)

    return parser.parse_args()

def from_timestamp(str):
    "时间戳转换为毫秒"
    l = str.split(":")
    if len(l) != 3:
        raise RuntimeError("错误的时间戳")
    hours, minutes , seconds = int(l[0]), int(l[1]), float(l[2])

    return (hours*3600 + minutes*60 + seconds) * 1000

def to_timestamp(sec):
    "毫秒转换时间戳"
    hours = sec//3600000
    minutes = (sec - hours * 3600000) // 60000
    seconds =  (sec - hours * 3600000 - minutes * 60000) // 1000
    r = ((sec - hours * 3600000 - minutes * 60000 - seconds * 1000)) // 10

    return "%d:%02d:%02d.%02d" % (hours, minutes, seconds, r)

def calc_correction(t1, t2, f1, f2):
    k = (t1 - t2) / (f1 - f2)
    b = t2 - k * f2
    return k, b

def correct_time(bad_timestamp, k, b):
    return bad_timestamp * k + b

def main():
    args = parse_args()

    if args.t1 == None or \
       args.t2 == None or \
       args.f1 == None or \
       args.f2 == None:
        raise RuntimeError("请输入字幕开始结束时间")

    k, b = calc_correction(args.t1, args.t2, args.f1, args.f2)

    with open(args.output, "w", encoding='utf-8') as fo:
        with open(args.input, "r", encoding='utf-8') as fi:
            for line in fi:
                line = line.rstrip()
                # print (line)
                m = re.match(r'^Dialogue: [0-9]+,([0-9]+:[0-9]+:[0-9]+(?:\.[0-9]+)?),([0-9]+:[0-9]+:[0-9]+(?:\.[0-9]+)?),', line)
                if m:
                    d1, d2 = from_timestamp(m.group(1)), from_timestamp(m.group(2))
                    nd1 = to_timestamp(correct_time(d1, k, b))
                    nd2 = to_timestamp(correct_time(d2, k, b))

                    line = line.replace(m.group(1), nd1, 1)
                    line = line.replace(m.group(2), nd2, 1)
                fo.write(line + "\n")
                

if __name__ == "__main__":
    main()
