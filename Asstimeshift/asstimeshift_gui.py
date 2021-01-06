#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import asstimeshift as ats
import os, subprocess
from functools import partial
import tkinter.messagebox
import threading
import json
import shutil
import sys

class Argument:
    pass

def mpv_runner(runlist):
    subprocess.call(runlist)

def get_showtime_lua_path():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'showtime.lua')

def get_json_path():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'config.json')

def get_output_ass_path(ass_path):
    return os.path.splitext(ass_path)[0] + ".fixed.ass"

DEFAULT_CONFIG = {
    "mpv" : "" if shutil.which('mpv') is None else shutil.which('mpv'),
    "ass_max_line" : 50,
}

def get_config_json():
    path = get_json_path()
    try:
        with open(path, "r") as fi:
            j = json.loads(fi.read())
    except Exception:
        j = DEFAULT_CONFIG

    return j

def save_config_json(config):
    path = get_json_path()
    j = json.dumps(config)
    with open(path, "w") as fo:
        fo.write(j)

CONFIG = get_config_json()

def get_dict_items(dict_, count, last=False):
    i = 0
    d = {}
    for k in sorted(dict_, reverse=last):
        d[k] = dict_[k]
        i += 1
        if i >= count:
            break
    return list(d.items())

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("AssTimeshift")
        self.master.resizable(False, False)

        self.l1 = []
        self.l2 = []
        self.input_filename = None
        self.media_filename = None

        self.create_widgets()

        if len(sys.argv) > 1:
            self.input_filename = sys.argv[1]
            self.output_filename = get_output_ass_path(self.input_filename)

        if self.input_filename is not None:
            self.get_f1_f2_lines()

    def call_mpv(self, seek_ts):
        if self.media_filename is None:
            tk.messagebox.showinfo('错误', '请设置媒体文件名')
            return

        seek_ts = seek_ts.get()
        seek_ts = 0 if seek_ts == "" else seek_ts
        seek_ts = ats.Timestamp(seek_ts)

        l = [ CONFIG['mpv'],
            "--script={}".format(get_showtime_lua_path()),
            "--pause",
            "--start={}".format(seek_ts.ts / 1000) ]
        if self.input_filename is not None:
            l.append("--sub-file={}".format(self.input_filename))
        l.append(self.media_filename)
        # print (l)
        t = threading.Thread(target=mpv_runner, args=(l,), daemon=True)
        t.start()

    def get_f1_f2_lines(self):
        "设置台词和时间戳显示"
        args = Argument()
        args.input = self.input_filename
        ass = ats.get_all_lines(args)
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, self.input_filename)

        self.l1 = get_dict_items(ass, CONFIG['ass_max_line']+1, False)
        self.line1.delete(0, tk.END)
        self.line1.insert(0, '0: {}'.format(self.l1[0][1]))

        self.l2 = get_dict_items(ass, CONFIG['ass_max_line']+1, True)
        self.line2.delete(0, tk.END)
        self.line2.insert(0, '0: {}'.format(self.l2[0][1]))

        t1 = f1 = self.l1[0][0]
        t2 = f2 = self.l2[0][0]
        self.f1.delete(0, tk.END)
        self.f1.insert(0, str(f1))
        self.t1.delete(0, tk.END)
        self.t1.insert(0, str(t1))
        self.f2.delete(0, tk.END)
        self.f2.insert(0, str(f2))
        self.t2.delete(0, tk.END)
        self.t2.insert(0, str(t2))

    def browserInput(self):
        filename = filedialog.askopenfilename(title = "选择输入字幕文件",
                                          filetypes = (("ASS文件",
                                                        "*.ass*"),
                                                       ("all files",
                                                        "*.*")))
        if not filename:
            return
        self.input_filename = filename
        self.output_filename = get_output_ass_path(self.input_filename)
        print (self.input_filename)
        print (self.output_filename)
        self.get_f1_f2_lines()

    def browserMedia(self):
        filename = filedialog.askopenfilename(title = "选择输入视频文件",
                                          filetypes = (("视频文件",
                                                        " .avi .mkv .mp4 .wmv .3gp .asf .flv .m4v .mpeg .mpg .rm .rmvb"),
                                                       ("all files",
                                                        "*.*")))
        if not filename:
            return
        self.media_filename = filename
        self.media.delete(0, tk.END)
        self.media.insert(0, str(self.media_filename))

    def spin1(self):
        i = int(self.line1.get())
        t1 = f1 = self.l1[i][0]
        self.f1.delete(0, tk.END)
        self.f1.insert(0, str(f1))
        self.t1.delete(0, tk.END)
        self.t1.insert(0, str(t1))
        self.line1.delete(0, tk.END)
        self.line1.insert(0, '{}: {}'.format(i, self.l1[i][1]))

    def spin2(self):
        i = int(self.line2.get())
        t2 = f2 = self.l2[i][0]
        self.f2.delete(0, tk.END)
        self.f2.insert(0, str(f2))
        self.t2.delete(0, tk.END)
        self.t2.insert(0, str(t2))
        self.line2.delete(0, tk.END)
        self.line2.insert(0, '{}: {}'.format(i, self.l2[i][1]))

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.master, text=' 字幕和媒体文件 ')
        input_frame.grid(column=0, row=0, columnspan=7, padx=2, pady=5)
        ttk.Label(input_frame, text='媒体文件').grid(column=0, row=0, sticky='W')
        self.media = ttk.Entry(input_frame, text='媒体文件', width=56*2)
        self.media.grid(column=1, row=0, columnspan=5)
        ttk.Button(input_frame, text='浏览', command=self.browserMedia).grid(column=6, row=0, sticky='W')

        ttk.Label(input_frame, text='字幕文件').grid(column=0, row=1, sticky='W')
        self.input_text = ttk.Entry(input_frame, text='字幕文件', width=56*2)
        self.input_text.grid(column=1, row=1, columnspan=5)
        ttk.Button(input_frame, text='浏览', command=self.browserInput).grid(column=6, row=1, sticky='W')

        for child in input_frame.winfo_children():
            child.grid_configure(padx=2, pady=1)

        time_frame = ttk.LabelFrame(self.master, text=' 字幕时间设置 ')
        time_frame.grid(column=0, row=1, columnspan=7, padx=2, pady=5)

        ttk.Label(time_frame, text='字幕原始时间1').grid(column=0, row=0, sticky='W')
        self.f1 = ttk.Entry(time_frame, text='字幕原始时间1', width=12)
        self.f1.grid(column=1, row=0, sticky='W')
        ttk.Label(time_frame, text='字幕目标时间1').grid(column=2, row=0, sticky='E')
        self.t1 = ttk.Entry(time_frame, text='字幕目标时间1', width=12)
        self.t1.grid(column=3, row=0, sticky='W')
        ttk.Button(time_frame, text='使用mpv播放段落1', command=partial(self.call_mpv, self.f1)).grid(column=4, row=0, sticky='E', columnspan=16)
        ttk.Label(time_frame, text='台词1').grid(column=0, row=1, sticky='W')
        self.line1 = ttk.Spinbox(time_frame, text='台词1', width=58*2, command=self.spin1, from_=0, to=CONFIG['ass_max_line'])
        self.line1.grid(column=1, row=1, columnspan=20-1, sticky='W')

        ttk.Label(time_frame, text='字幕原始时间2').grid(column=0, row=2, sticky='W')
        self.f2 = ttk.Entry(time_frame, text='字幕原始时间2', width=12)
        self.f2.grid(column=1, row=2, sticky='W')
        ttk.Label(time_frame, text='字幕目标时间2').grid(column=2, row=2, sticky='E')
        self.t2 = ttk.Entry(time_frame, text='字幕目标时间2', width=12)
        self.t2.grid(column=3, row=2, sticky='W')
        ttk.Button(time_frame, text='使用mpv播放段落2', command=partial(self.call_mpv, self.f2)).grid(column=4, row=2, sticky='E', columnspan=16)
        ttk.Label(time_frame, text='台词2').grid(column=0, row=3, sticky='W')
        self.line2 = ttk.Spinbox(time_frame, text='台词2', width=58*2, command=self.spin2, from_=0, to=CONFIG['ass_max_line'])
        self.line2.grid(column=1, row=3, columnspan=20-1, sticky='W')

        for child in time_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)

        def config_window():
            def browserMPV():
                filename = filedialog.askopenfilename(title = "选择MPV",
                                                  filetypes = (
                                                               ("all files",
                                                                "*.*"),))
                if not filename:
                    return
                mpv.delete(0, tk.END)
                mpv.insert(0, filename)

            def save_and_destroy():
                CONFIG['mpv'] = mpv.get()
                CONFIG['ass_max_line'] = int(ass_max_line.get())
                save_config_json(CONFIG)

                # 重设self.line1和self.line2的to属性
                self.line1['to'] = CONFIG['ass_max_line']
                self.line2['to'] = CONFIG['ass_max_line']

                if self.input_filename:
                    self.get_f1_f2_lines()

                config_win.destroy()

            config_win = tk.Tk()
            config_win.resizable(False, False)
            config_win.title("配置")

            mpv_frame = ttk.LabelFrame(config_win, text=' 字幕配置 ')
            mpv_frame.grid(column=0, row=0, padx=2, pady=5, columnspan=2)

            ttk.Label(mpv_frame, text='MPV可执行文件路径: ').grid(column=0, row=0, sticky='W')
            mpv = ttk.Entry(mpv_frame)
            mpv.grid(column=1, row=0)
            mpv.delete(0, tk.END)
            mpv.insert(0, CONFIG['mpv'])
            ttk.Button(mpv_frame, text='浏览', command=browserMPV).grid(column=2, row=0, sticky='W')

            ttk.Label(mpv_frame, text='最大字幕个数: ').grid(column=0, row=1, sticky='W')
            ass_max_line = ttk.Spinbox(mpv_frame, width=28, from_=0, to=999)
            ass_max_line.grid(column=1, row=1, columnspan=2)
            ass_max_line.delete(0, tk.END)
            ass_max_line.insert(0, CONFIG['ass_max_line'])

            cancel = ttk.Button(config_win, text='取消', command=config_win.destroy)
            cancel.grid(column=0, row=2)
            save = ttk.Button(config_win, text='保存', command=save_and_destroy)
            save.grid(column=1, row=2)
            config_win.bind('<Escape>', lambda x: config_win.destroy())
            config_win.mainloop()

        config = ttk.Button(self.master, text='配置', command=config_window)
        config.grid(column=0, row=5, sticky='W')
        convert = ttk.Button(self.master, text='转化', command=self.process_ass).grid(column=3, row=5)
        quit = ttk.Button(self.master, text='退出', command=self.master.destroy)
        quit.grid(column=6, row=5, sticky='E')

        self.input_frame = input_frame
        self.time_frame = time_frame

    def process_ass(self):
        try:
            args = Argument()
            args.input = self.input_filename
            args.output = self.output_filename
            args.t1 = ats.Timestamp(self.t1.get())
            args.t2 = ats.Timestamp(self.t2.get())
            args.f1 = ats.Timestamp(self.f1.get())
            args.f2 = ats.Timestamp(self.f2.get())

            try:
                with open(args.output, "w", encoding='utf-8') as fo:
                    with open(args.input, "r", encoding='utf-8') as fi:
                        warns = ats.asstimeshift(args, fi, fo)
            except UnicodeDecodeError:
                with open(args.input, "rb") as fi:
                    b = fi.read()
                with open(args.output, "w", encoding='utf-8') as fo:
                    with open(args.input, "r", encoding=ats.chardet_detect(b)) as fi:
                        warns = ats.asstimeshift(args, fi, fo)

            tk.messagebox.showinfo('提示', '转换完成:\n{}\n{}'.format(self.output_filename, "\n".join(warns)))
        except Exception as e:
            tk.messagebox.showerror('错误', '转换失败:\n{}'.format(str(e)))
            raise (e)

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()

# vim: set sw=4 tabstop=4 expandtab :
