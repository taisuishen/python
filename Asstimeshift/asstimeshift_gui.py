#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import asstimeshift as ats
import os, subprocess
from functools import partial
import tkinter.messagebox
import threading

MPV = r"/usr/bin/mpv"

class Argument:
    pass

def mpv_runner(runlist):
    subprocess.call(runlist)

def get_showtime_lua_path():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'showtime.lua')

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.media_filename = None
        self.master.title("AssTimeshift")
        self.create_widgets()
        self.l1 = []
        self.l2 = []

    def call_mpv(self, seek_ts):
        if self.media_filename is None:
            tk.messagebox.showinfo('错误', '请设置媒体文件名')
            return

        seek_ts = ats.Timestamp(seek_ts.get())
        subfn = self.input_filename
        l = [ MPV,
            "--script={}".format(get_showtime_lua_path()),
            "--pause",
            "--start={}".format(seek_ts.ts / 1000),
            "--sub-file={}".format(subfn), self.media_filename ]
        # print (l)
        t = threading.Thread(target=mpv_runner, args=(l,), daemon=True)
        t.start()

    def get_f1_f2_lines(self):
        "获取字幕的起始字幕和最后字幕，并设置台词显示"
        args = Argument()
        args.input = self.input_filename
        ass = ats.get_all_lines(args)
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, self.input_filename)

        i = 0
        self.l1 = {}
        for k in sorted(ass):
            self.l1[k] = ass[k]
            i += 1
            if i > 20:
                break

        self.l1 = list(self.l1.items())
        self.line1.delete(0, tk.END)
        self.line1.insert(0, '0: {}'.format(self.l1[0][1]))

        i = 0
        self.l2 = {}
        for k in sorted(ass, reverse=True):
            self.l2[k] = ass[k]
            i += 1
            if i > 20:
                break

        self.l2 = list(self.l2.items())
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
        self.output_filename = os.path.splitext(filename)[0] + ".fixed.ass"
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
        self.media = ttk.Entry(input_frame, text='媒体文件', width=56)
        self.media.grid(column=1, row=0, columnspan=5)
        ttk.Button(input_frame, text='浏览', command=self.browserMedia).grid(column=6, row=0, sticky='W')

        ttk.Label(input_frame, text='字幕文件').grid(column=0, row=1, sticky='W')
        self.input_text = ttk.Entry(input_frame, text='字幕文件', width=56)
        self.input_text.grid(column=1, row=1, columnspan=5)
        ttk.Button(input_frame, text='浏览', command=self.browserInput).grid(column=6, row=1, sticky='W')

        for child in input_frame.winfo_children():
            child.grid_configure(padx=2, pady=1)

        time_frame = ttk.LabelFrame(self.master, text=' 字幕时间设置 ')
        time_frame.grid(column=0, row=1, columnspan=7, padx=2, pady=5)

        ttk.Label(time_frame, text='字幕原始时间1').grid(column=0, row=0, sticky='W')
        self.f1 = ttk.Entry(time_frame, text='字幕原始时间1', width=16)
        self.f1.grid(column=1, row=0, sticky='W')
        ttk.Label(time_frame, text='字幕目标时间1').grid(column=2, row=0, sticky='W')
        self.t1 = ttk.Entry(time_frame, text='字幕目标时间1', width=16)
        self.t1.grid(column=3, row=0, sticky='W')
        ttk.Button(time_frame, text='mpv段落1', width=16, command=partial(self.call_mpv, self.f1)).grid(column=4, row=0, sticky='W')
        ttk.Label(time_frame, text='台词1').grid(column=0, row=1, sticky='W')
        self.line1 = ttk.Spinbox(time_frame, text='台词1', width=60, command=self.spin1, from_=0, to=20)
        self.line1.grid(column=1, row=1, columnspan=4, sticky='W')

        ttk.Label(time_frame, text='字幕原始时间2').grid(column=0, row=2, sticky='W')
        self.f2 = ttk.Entry(time_frame, text='字幕原始时间2', width=16)
        self.f2.grid(column=1, row=2, sticky='W')
        ttk.Label(time_frame, text='字幕目标时间2').grid(column=2, row=2, sticky='W')
        self.t2 = ttk.Entry(time_frame, text='字幕目标时间2', width=16)
        self.t2.grid(column=3, row=2, sticky='W')
        ttk.Button(time_frame, text='mpv段落2', width=16, command=partial(self.call_mpv, self.f2)).grid(column=4, row=2, sticky='W')
        ttk.Label(time_frame, text='台词2').grid(column=0, row=3, sticky='W')
        self.line2 = ttk.Spinbox(time_frame, text='台词2', width=60, command=self.spin2, from_=0, to=20)
        self.line2.grid(column=1, row=3, columnspan=4, sticky='W')

        for child in time_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)

        def config_window():
            config_win = tk.Tk()
            config_win.resizable(False, False)
            config_win.title("配置")

            mpv_frame = ttk.LabelFrame(config_win, text=' MPV ')
            mpv_frame.grid(column=0, row=0, columnspan=7, padx=2, pady=5)

            ttk.Label(mpv_frame, text='MPV可执行文件路径').grid(column=0, row=0, sticky='W')
            ttk.Entry(mpv_frame, width=20).grid(column=1, row=0, columnspan=5)
            ttk.Button(mpv_frame, text='浏览').grid(column=6, row=0, sticky='W')

            cancel = ttk.Button(config_win, text='取消', command=config_win.destroy)
            cancel.grid(column=0, row=1)
            save = ttk.Button(config_win, text='保存', command=config_win.destroy)
            save.grid(column=1, row=1)
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
        args = Argument()
        args.input = self.input_filename
        args.output = self.output_filename
        args.t1 = ats.Timestamp(self.t1.get())
        args.t2 = ats.Timestamp(self.t2.get())
        args.f1 = ats.Timestamp(self.f1.get())
        args.f2 = ats.Timestamp(self.f2.get())

        with open(args.output, "w", encoding='utf-8') as fo:
            with open(args.input, "r", encoding='utf-8') as fi:
                ats.asstimeshift(args, fi, fo)

        tk.messagebox.showinfo('提示', '转换完成:\n{}'.format(self.output_filename))

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()

# vim: set sw=4 tabstop=4 expandtab :
