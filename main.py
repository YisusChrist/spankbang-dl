import requests
import re
from concurrent.futures import ThreadPoolExecutor
import os, time
import shutil
from tqdm import tqdm
#引入库

headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
#引入 headers

url=input("请输入Spankbang地址:")
r=requests.get(url,headers=headers)
if r.status_code==200:
    print("网页内容抓取成功！"+str(r.status_code))
else:
    print("网页内容抓取失败！"+str(r.status_code))
#判断是否正常抓取

html=r.text
result=re.search('<video.*?src="(.*?)".*?>.*?</video>',html,re.S)
src=result.group(1)
#获取到视频链接

result2=re.search('<title.*?>Watch(.*?) - .*?</title.*?>',html,re.S)
title=result2.group(1)
#获取到网页title

def save_video(title):
    try:
        print("准备下载视频",title)
        resp = requests.get(src,stream=True)
        content_size = int(resp.headers['Content-Length'])/1048576
        with open(title + '.mp4',mode='wb') as f:
            print("总大小是:",content_size,'mb,开始...')
            for data in tqdm(iterable=resp.iter_content(1048576),total=content_size,unit='mb',desc=title):
                f.write(data)
        print(title,"视频保存完成")
    except Exception:
        print("下载视频失败")
#下载保存视频

a=input(f"\n是否要下载{title}(此视频)[y/n]:")
if a=='y':
    save_video(title)
else:
    print("请关掉重新打开以下载视频")
#主程序
