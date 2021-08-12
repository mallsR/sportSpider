from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request,urllib.error
import uuid
import datetime
import os
import codecs
import requests
import re

def newsSpider(task, news_num, video_num, player_num, game_num):
    if task[8] == '1':
        news_num = nSpider1(task, news_num)
    elif task[8] == '2':
        news_num = nSpider2(task, news_num)
    elif task[8] == '3':
        news_num = nSpider3(task, news_num)
    return news_num, video_num, player_num, game_num

def nSpider1(task, news_num): #爬取新闻稿
    textlist = []
    news = Article(task[0], language='zh')
    news.download()        # 加载网页
    news.parse()           # 解析网页
    textlist.append(news.title)     #保存题目
    textlist.append(news.text)      #保存正文
    saveText(textlist)              #保存到本地
    news_num += 1
    return news_num

def nSpider2(task, news_num):
    sn_task_list = get_sn_url(task) #找到所有二级链接
    for sn_task in sn_task_list:
        news_num = nSpider1([sn_task], news_num)           #对每一条爬取新闻稿
    return news_num

def nSpider3(task, news_num):
    tn_task_list = get_tn_url(task) #找到所有三级链接
    for tn_task in tn_task_list:
        news_num = nSpider1([tn_task], news_num)           #对每一条爬取新闻稿
    return news_num

def saveText(textlist):
    if textlist[1] != '':
        file_name = uuid.uuid1()
        path = getpath()
        with codecs.open('%s\\%s.txt'%(path,file_name), mode='a', encoding='utf-8') as file_txt:
            file_txt.write(textlist[0]+'\n')
            file_txt.write(textlist[1])
    else:
        pass

def getpath():
    today_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H'))
    path = 'C:\\Users\\gao\\Desktop\\bysj\\result\\%sresult\\news'%today_date
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return path

def judge(url):
    try:
        head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
        html = requests.get(url,headers=head)
        html.raise_for_status()
        html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。    
        soup = BeautifulSoup(html.text,"html.parser")
        jugdestr = str(soup.find_all('title')[0])
        title = '举重'
        flag = title in jugdestr
    except:
        flag = False
    return flag

def get_sn_url(task):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    findUrl = re.compile(r'<(.*?)href="(.*?)"(.*?)')
    urllist = []
    sn_task_list = []
    html = requests.get(task[0],headers=head)
    html.raise_for_status()
    html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。
    soup = BeautifulSoup(html.text,"html.parser")
    for item in soup.find_all('body'):
        item = str(item)
        url = re.findall(findUrl,item)  #找到所有链接
        for i in url:                   #处理每一条找到的链接
            url_2 = i[1]
            if url_2[0:4] != "http":
                url_2 = "https:" + url_2
            if url_2[0:6] == "http:/":
                urllist.append(url_2)
            if url_2[0:7] == "https:/":
                urllist.append(url_2)
    for i in urllist:                   #对于找到的所有链接
        flag = judge(i)                 #判断是否为举重相关
        if flag:
            if i not in sn_task_list:   #如果链接不在二级列表中
                sn_task_list.append(i)  #添加到二级链接列表
    return sn_task_list

def get_tn_url(task):
    sn_task_list = get_sn_url(task) #找到所有二级链接
    tn_task_list = sn_task_list     #三级链接包含所有二级链接
    for sn_task in sn_task_list:    #对于每一个二级链接
        item_list = get_sn_url(sn_task) #找到对应的三级链接
        for item_task in item_list:     #对于找到的三级链接
            if item_task not in tn_task_list:   #如果不在结果列表中
                tn_task_list.append(item_task)  #添加到三级链接列表
    return tn_task_list

if __name__ == "__main__":
    task1 = ['http://www.cwa.org.cn/index.html','举重','news','2021053021','2021053021','2021053021','waiting','24','1','run','0121']
    task = ['http://www.cwa.org.cn/zhongguoliliang/','举重','news','2021053021','2021053021','2021053021','waiting','24','2','run','0123']
    newsSpider(task)