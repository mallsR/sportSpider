from bs4 import BeautifulSoup
import re
import requests
import datetime
import os
import codecs


# 爬取运动员的信息，应该不需要三个不同的爬虫，需要考虑合并为一个
def player1Spider(task, news_num, video_num, player_num, game_num):
    play_list = []
    level_list = []
    findname = re.compile(r'''中文名</dt>
(.*?)>
(.*?)
</dd>''')
    findbirthday = re.compile(r'''出生日期</dt>
(.*?)>
(.*?)
</dd>''')
    findteam = re.compile(r'''所属运动队</dt>
(.*?)>
(.*?)
</dd>''')
    findlevel = re.compile(r'''(\d*)公斤级''')
    findbestre = re.compile(r'''(\d*)公斤''')
    soup = getsoup(task)
    for item in soup.find_all('body'):
        item = str(item)
        name = re.findall(findname, item)
        if name != []:
            play_list.append(name[0][1])
        birthday = re.findall(findbirthday, item)
        if birthday != []:
            play_list.append(birthday[0][1])
        team = re.findall(findteam, item)
        if team != []:
            play_list.append(team[0][1])
        level = ''
        _level = re.findall(findlevel, item)
        for i in _level:
            try:
                i = int(i)
                if i not in level_list:
                    level_list.append(i)
            except:
                pass
        for j in level_list:
            level = level + "男子%d公斤级 "%j
        play_list.append(level)
        _bestre = re.findall(findbestre, item)
        a = 0
        for k in _bestre:
            try:
                if int(k) > a:
                    a = int(k)
            except:
                pass
        bestre = "总成绩%d公斤"%a
        play_list.append(bestre)
    saveText(play_list)              #保存到本地
    player_num += 1
    return news_num, video_num, player_num, game_num

def player2Spider(task, news_num, video_num, player_num, game_num):
    play_list = []
    level_list = []
    findname = re.compile(r'''中文名</dt>
(.*?)>
(.*?)
</dd>''')
    findbirthday = re.compile(r'''(\d*)年(.*?)出生''')
    findteam = re.compile(r'''所属运动队</dt>''')
#     findlevel = re.compile(r'''专业特点</dt>
# (.*?)>
# (.*?)
# </dd>''')
    findlevel = re.compile(r'''(\d*)公斤级''')
    findbestre = re.compile(r'''(\d*)公斤''')
    soup = getsoup(task)
    for item in soup.find_all('body'):
        item = str(item)
        name = re.findall(findname, item)
        if name != []:
            play_list.append(name[0][1])
        birthday = re.findall(findbirthday, item)
        if birthday != []:
            play_list.append(birthday[0][0]+'年')
        team = '中国国家举重队'
        play_list.append(team)
        level = re.findall(findlevel, item)
        if level != []:
            play_list.append(level[0][1])
        _bestre = re.findall(findbestre, item)
        a = 0
        for k in _bestre:
            try:
                if int(k) > a:
                    a = int(k)
            except:
                pass
        bestre = "总成绩%d公斤" % a
        play_list.append(bestre)
    saveText(play_list)              #保存到本地
    player_num += 1
    return news_num, video_num, player_num, game_num

def player3Spider(task, news_num, video_num, player_num, game_num):
    play_list = []
    level_list = []
    findname = re.compile(r'''中文名</dt>
(.*?)>
(.*?)
</dd>''')
    findbirthday = re.compile(r'''出生日期</dt>
(.*?)>
(.*?)
</dd>''')
    findteam = re.compile(r'''所属运动队</dt>''')
    findlevel = re.compile(r'''(\d*)公斤级''')
    findbestre = re.compile(r'''(\d*)公斤''')
    soup = getsoup(task)
    for item in soup.find_all('body'):
        item = str(item)
        name = re.findall(findname, item)
        if name != []:
            play_list.append(name[0][1])
        birthday = re.findall(findbirthday, item)
        if birthday != []:
            play_list.append(birthday[0][1])
        team = '中国国家举重队'
        play_list.append(team)
        level = ''
        _level = re.findall(findlevel, item)
        for i in _level:
            try:
                i = int(i)
                if i not in level_list:
                    level_list.append(i)
            except:
                pass
        for j in level_list:
            level = level + "女子%d公斤级 "%j
        play_list.append(level)
        _bestre = re.findall(findbestre, item)
        a = 0
        for k in _bestre:
            try:
                if int(k) > a:
                    a = int(k)
            except:
                pass
        bestre = "总成绩%d公斤" % a
        play_list.append(bestre)
    saveText(play_list)              #保存到本地
    player_num += 1
    return news_num, video_num, player_num, game_num

def getsoup(task):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    html = requests.get(task[0],headers=head)
    html.raise_for_status()
    html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。
    soup = BeautifulSoup(html.text,"html.parser")
    return soup

def saveText(play_list):
    file_name = play_list[0]
    path = getpath()
    with codecs.open('%s/%s.txt'%(path,file_name), mode='a', encoding='utf-8') as file_txt:
        for text in play_list:
            file_txt.write(text+'\n')

def getpath():
    today_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H'))
    # path = 'C:\\Users\\gao\\Desktop\\bysj\\result\\%sresult\\player'%today_date
    path = ('/Users/xiaor/Project/Laboratory_project/result/%sresult/player' % today_date).replace(' ', '_')
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return path

if __name__ == "__main__":
    task = ['https://baike.baidu.com/item/%E8%92%8B%E6%83%A0%E8%8A%B1/9620518?fr=aladdin']
    player3Spider(task)