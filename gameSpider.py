from bs4 import BeautifulSoup
import re
import requests
import uuid
import datetime
import os
import codecs
import urllib.request

def game1Spider(task, news_num, video_num, player_num, game_num):
    findsrc = re.compile(r'''src="(.*?)"/>
</p>
<p class="one-p">最终比赛成绩 图源视频截图</p>''')
    srclist = []
    soup = getsoup(task)
    for item in soup:
        item = str(item)
        src = re.findall(findsrc, item)
        if src != []:
            src[0] = "https:" + src[0]
            if src not in srclist:
                srclist.append(src)
    saveSrc(srclist)
    game_num += 1
    return news_num, video_num, player_num, game_num

def getsoup(task):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    html = requests.get(task[0],headers=head)
    html.raise_for_status()
    html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。
    soup = BeautifulSoup(html.text,"html.parser")
    return soup

def saveSrc(srclist):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    imgsrc = srclist[0][0]
    file_name = str(uuid.uuid1())
    path = getpath()
    requesti = urllib.request.Request(imgsrc,headers=head)
    f = open("%s\\%s.jpg"%(path, file_name),'wb')
    f.write(urllib.request.urlopen(requesti).read())
    f.close()

def getpath():
    today_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H'))
    path = 'C:\\Users\\gao\\Desktop\\bysj\\result\\%sresult\\game'%today_date
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return path

if __name__ == "__main__":
    task = ['https://new.qq.com/omn/20210418/20210418A01F8I00.html']
    game1Spider(task)