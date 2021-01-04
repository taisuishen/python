import tkinter as tk
from tkinter import filedialog 
import asstimeshift as ats
import os, subprocess
from functools import partial
import tkinter.messagebox 

MPV = r"C:\Temp\mpv-withassrt\mpv.com"

class Argument:
    pass
    
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.media_filename = None

        self.pack()
        self.create_widgets()
        
    def call_mpv(self, seek_ts):
        if self.media_filename is None:
            tk.messagebox.showinfo('错误', '请设置媒体文件名')
            return
            
        seek_ts = ats.Timestamp(seek_ts.get())
        path = self.input_filename
        l = [MPV, "--pause", 
            "--start={}".format(seek_ts.ts / 1000),
            "--sub-file={}".format(path), self.media_filename]
        # print (l)
        subprocess.call(l)
    
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
        self.input_filename = filename
        self.output_filename = os.path.splitext(filename)[0] + ".fixed.ass"
        print (self.input_filename)
        print (self.output_filename)
        self.get_f1_f2_lines()
        
    def browserMedia(self):
        filename = filedialog.askopenfilename(title = "选择输入视频文件", 
                                          filetypes = (("视频文件", 
                                                        "*.mkv*"), 
                                                       ("all files", 
                                                        "*.*"))) 
        self.media_filename = filename
        self.media.delete(0, tk.END)
        self.media.insert(0, str(self.media_filename))
        
    def create_widgets(self):
        self.input_text = tk.Entry(self)
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, "字幕文件名")
        self.input_text.pack()
        self.input_browser = tk.Button(self)
        self.input_browser["text"] = "浏览字幕文件"
        self.input_browser["command"] = self.browserInput
        self.input_browser.pack()
        
        self.media = tk.Entry(self)
        self.media.delete(0, tk.END)
        self.media.insert(0, "媒体文件名")
        self.media.pack()
        self.media_browser = tk.Button(self)
        self.media_browser["text"] = "浏览媒体文件"
        self.media_browser["command"] = self.browserMedia
        self.media_browser.pack()
        
        self.f1 = tk.Entry(self)
        self.f1.pack()
        
        self.t1 = tk.Entry(self)
        self.t1.pack()
        
        self.line1 = tk.Entry(self)
        self.line1.pack()
        
        self.mpv1 = tk.Button(self)
        self.mpv1["text"] = "mpv1"
        self.mpv1["command"] = partial(self.call_mpv, self.f1)
        self.mpv1.pack()
        
        self.f2 = tk.Entry(self)
        self.f2.pack()
        
        self.t2 = tk.Entry(self)
        self.t2.pack()
        
        self.line2 = tk.Entry(self)
        self.line2.pack()
        
        self.mpv2 = tk.Button(self)
        self.mpv2["text"] = "mpv2"
        self.mpv2["command"] = partial(self.call_mpv, self.f2)
        self.mpv2.pack()

        self.convert = tk.Button(self)
        self.convert["text"] = "转换字幕"
        self.convert["command"] = self.process_ass
        self.convert.pack()
        
        self.quit = tk.Button(self, text="退出", fg="red",
                              command=self.master.destroy)
        self.quit.pack()

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
