import tkinter as tk
from tkinter import filedialog 
import asstimeshift as ats
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.pack()
        self.create_widgets()
    
    def get_f1_f2_lines(self):
        "获取字幕的起始字幕和最后字幕，并设置台词显示"
        pass
    
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
        
    def create_widgets(self):
        self.input_text = tk.Entry(self)
        self.input_text["text"] = "字幕文件名"
        self.input_text.pack()
        self.input_browser = tk.Button(self)
        self.input_browser["text"] = "浏览字幕文件"
        self.input_browser["command"] = self.browserInput
        self.input_browser.pack()
        
        self.f1 = tk.Entry(self)
        self.f1["text"] = "f1"
        self.f1.pack()
        
        self.t1 = tk.Entry(self)
        self.t1["text"] = "t1"
        self.t1.pack()
        
        self.line1 = tk.Entry(self)
        self.line1["text"] = "line1"
        self.line1.pack()
        
        self.mpv1 = tk.Button(self)
        self.mpv1["text"] = "mpv1"
        self.mpv1.pack()
        
        self.f2 = tk.Entry(self)
        self.f2["text"] = "f2"
        self.f2.pack()
        
        self.t2 = tk.Entry(self)
        self.t2["text"] = "t2"
        self.t2.pack()
        
        self.line2 = tk.Entry(self)
        self.line2["text"] = "line2"
        self.line2.pack()
        
        self.mpv2 = tk.Button(self)
        self.mpv2["text"] = "mpv1"
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

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    
if __name__ == "__main__":
    main()
