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

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.media_filename = None
        self.master.title("AssTimeshift")
        self.create_widgets()

    def call_mpv(self, seek_ts):
        if self.media_filename is None:
            tk.messagebox.showinfo('错误', '请设置媒体文件名')
            return

        seek_ts = ats.Timestamp(seek_ts.get())
        subfn = self.input_filename
        l = [ MPV,
            "--script=showtime.lua",
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
        f1, f2, f1_line, f2_line = ats.get_min_max_ass_line(args)
        # print (f1, f2, f1_line, f2_line)

        t1 = f1
        t2 = f2

        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, self.input_filename)

        self.f1.delete(0, tk.END)
        self.f1.insert(0, str(f1))
        self.t1.delete(0, tk.END)
        self.t1.insert(0, str(t1))

        self.line1.delete(0, tk.END)
        self.line1.insert(0, str(f1_line))

        self.f2.delete(0, tk.END)
        self.f2.insert(0, str(f2))
        self.t2.delete(0, tk.END)
        self.t2.insert(0, str(t2))

        self.line2.delete(0, tk.END)
        self.line2.insert(0, str(f2_line))

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
        self.line1 = ttk.Spinbox(time_frame, text='台词1', width=60)
        self.line1.grid(column=1, row=1, columnspan=4, sticky='W')

        ttk.Label(time_frame, text='字幕原始时间2').grid(column=0, row=2, sticky='W')
        self.f2 = ttk.Entry(time_frame, text='字幕原始时间2', width=16)
        self.f2.grid(column=1, row=2, sticky='W')
        ttk.Label(time_frame, text='字幕目标时间2').grid(column=2, row=2, sticky='W')
        self.t2 = ttk.Entry(time_frame, text='字幕目标时间2', width=16)
        self.t2.grid(column=3, row=2, sticky='W')
        ttk.Button(time_frame, text='mpv段落2', width=16, command=partial(self.call_mpv, self.f2)).grid(column=4, row=2, sticky='W')
        ttk.Label(time_frame, text='台词2').grid(column=0, row=3, sticky='W')
        self.line2 = ttk.Spinbox(time_frame, text='台词2', width=60)
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
        print("开始转化")

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

        tk.messagebox.showinfo('提示', '转换完成')

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
