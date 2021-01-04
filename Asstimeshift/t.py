#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

win = tk.Tk()
win.resizable(False, False)

win.title("ASS字幕Timeshift")

input_frame = ttk.LabelFrame(win, text=' 字幕和媒体文件 ')
input_frame.grid(column=0, row=0, columnspan=7, padx=2, pady=5)
ttk.Label(input_frame, text='媒体文件').grid(column=0, row=0, sticky='W')
ttk.Entry(input_frame, text='媒体文件', width=56).grid(column=1, row=0, columnspan=5)
ttk.Button(input_frame, text='浏览').grid(column=6, row=0, sticky='W')

ttk.Label(input_frame, text='字幕文件').grid(column=0, row=1, sticky='W')
ttk.Entry(input_frame, text='字幕文件', width=56).grid(column=1, row=1, columnspan=5)
ttk.Button(input_frame, text='浏览').grid(column=6, row=1, sticky='W')

for child in input_frame.winfo_children():
    child.grid_configure(padx=2, pady=1)

time_frame = ttk.LabelFrame(win, text=' 字幕时间设置 ')
time_frame.grid(column=0, row=1, columnspan=7, padx=2, pady=5)

ttk.Label(time_frame, text='字幕原始时间1').grid(column=0, row=0, sticky='W')
ttk.Entry(time_frame, text='字幕原始时间1', width=16).grid(column=1, row=0, sticky='W')
ttk.Label(time_frame, text='字幕目标时间1').grid(column=2, row=0, sticky='W')
ttk.Entry(time_frame, text='字幕目标时间1', width=16).grid(column=3, row=0, sticky='W')
ttk.Button(time_frame, text='mpv段落1', width=16).grid(column=4, row=0, sticky='W')
ttk.Label(time_frame, text='台词1').grid(column=0, row=1, sticky='W')
ttk.Spinbox(time_frame, text='台词1', width=60).grid(column=1, row=1, columnspan=4, sticky='W')

ttk.Label(time_frame, text='字幕原始时间2').grid(column=0, row=2, sticky='W')
ttk.Entry(time_frame, text='字幕原始时间2', width=16).grid(column=1, row=2, sticky='W')
ttk.Label(time_frame, text='字幕目标时间2').grid(column=2, row=2, sticky='W')
ttk.Entry(time_frame, text='字幕目标时间2', width=16).grid(column=3, row=2, sticky='W')
ttk.Button(time_frame, text='mpv段落2', width=16).grid(column=4, row=2, sticky='W')
ttk.Label(time_frame, text='台词2').grid(column=0, row=3, sticky='W')
ttk.Spinbox(time_frame, text='台词2', width=60).grid(column=1, row=3, columnspan=4, sticky='W')

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

config = ttk.Button(win, text='配置', command=config_window)
config.grid(column=0, row=5, sticky='W')
convert = ttk.Button(win, text='转化').grid(column=3, row=5)
quit = ttk.Button(win, text='退出', command=win.destroy)
quit.grid(column=6, row=5, sticky='E')

win.mainloop()
