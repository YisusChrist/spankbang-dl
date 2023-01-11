import requests
import re
import os, time
from tqdm import tqdm
from tqdm.gui import tqdm
import sys
#引入库

#写UI
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox
from tkinter import filedialog as fDialog

win = tk.Tk()
win.title("Spankbang视频下载器")
win.resizable(0,0)
#创建窗口

#创建输入视频网站地址的输入框
aLabel = ttk.Label(win, text="请输入Spankbang视频地址:")
aLabel.grid(column=0, row=0)
a_url = ttk.Entry(win)
a_url.grid(column=1, row=0)

#创建一个下载进度显示框
scrolW = 50
scrolH = 3
scr = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=0,row=1,columnspan=2)

#创建一个下载按钮
def _download():
    url = a_url.get()
    try:
        headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        r=requests.get(url,headers=headers)
        if r.status_code==200:
            scr.insert(tk.INSERT, "网页内容抓取成功！"+str(r.status_code)+"\n")
            html=r.text
            result=re.findall('<video.*?src="(.*?)".*?>.*?</video>',html,re.S)[0] #获取视频地址
            title=re.findall('<title.*?>Watch(.*?) - .*?</title.*?>',html,re.S)[0]#获取视频标题
            scr.insert(tk.INSERT, "视频标题:"+title+"\n")
            scr.insert(tk.INSERT, "视频地址:"+result+"\n")
            resp = requests.get(result,stream=True)
            content_size = int(resp.headers['Content-Length'])/1048576
            with open(title + '.mp4',mode='wb') as f:
                scr.insert(tk.INSERT, "总大小是:"+str(content_size)+"mb,开始...\n")
                for data in tqdm(iterable=resp.iter_content(1048576),total=content_size,unit='mb',desc=title,gui=True,leave=False,position=1, file=sys.stdout):
                    f.write(data)
                scr.insert(tk.INSERT, "视频下载完成！\n")
        else:
            scr.insert(tk.INSERT, "网页内容抓取失败！" + str(r.status_code) + "\n")
    except requests.exceptions.RequestException as e:
        scr.insert(tk.INSERT, "下载失败！错误信息："+ str(e) + "\n")
        
def _quit():
    win.quit()
    win.destroy()
    exit()
#退出程序

def _about():
    mBox.showinfo('关于','作者：@星\n版本：1.0\n更新时间：2022/1/11')
#关于

def _help():
    mBox.showinfo('帮助','1.输入Spankbang视频地址\n2.点击下载\n3.等待下载完成')
#帮助
action = ttk.Button(win, text="下载", command=_download)
action.grid(column=0, row=2)
#创建一个退出按钮
action2 = ttk.Button(win, text="退出", command=_quit)
action2.grid(column=1, row=2)
#创建一个关于按钮
action3 = ttk.Button(win, text="关于", command=_about)
action3.grid(column=0, row=3)
#创建一个帮助按钮
action4 = ttk.Button(win, text="帮助", command=_help)
action4.grid(column=1, row=3)

#创建一个菜单栏
menuBar = Menu(win)
win.config(menu=menuBar)


win.mainloop()
