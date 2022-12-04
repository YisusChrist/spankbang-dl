import requests
import re
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

result2=re.search('<title.*?>(.*?) - .*?</title.*?>',html,re.S)
title=result2.group(1)
#获取到网页title

url_video=requests.get(src,stream=True)
#解析视频二进制文件

def save_video(title,url_video):
    try:
        print("准备下载视频",title)
        print('十分抱歉本人实力有限，进度条还没有做好，请耐心等待')
        url_content=url_video.content#二进制url_video
        with open(title + '.mp4',mode='wb') as f:
            f.write(url_content)
        print(title,"视频保存完成")
    except Exception:
        print("下载视频失败")
#下载保存视频

a=input(f"\n是否要下载{title}(此视频)[y/n]:")
if a=='y':
    save_video(title,url_video)
else:
    print("请关掉重新打开以下载视频")
#主程序