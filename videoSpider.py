from bs4 import BeautifulSoup
import sys
import you_get
import os
import requests
import datetime
import re

def videoSpider(task, news_num, video_num, player_num, game_num):
    path = getpath()
    if task[8] == "1":  #下载视频
        sys.argv = ['you-get', '-o', path, task[0]]
        you_get.main()
        video_num += 1
    if task[8] == "2":
        sv_url_list = get_sv_url(task[0])   #找到所有二级链接
        # print(sv_url_list)
        for sv_url in sv_url_list:          #下载每一条二级链接中的视频
            try:
                sys.argv = ['you-get', '-o', path, sv_url]
                you_get.main()
                video_num += 1
            except:
                pass
    elif task[8] == "3":
        tv_url_list = get_tv_url(task[0])   #找到所有三级链接
        for tv_url in tv_url_list:          #下载每一条三级链接中的视频
            try:
                sys.argv = ['you-get', '-o', path, tv_url]
                you_get.main()
                video_num += 1
            except:
                pass
    return news_num, video_num, player_num, game_num

def getpath():
    today_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H'))
    # path = 'C:\\Users\\gao\\Desktop\\bysj\\result\\%sresult\\video'%today_date
    path = ('/Users/xiaor/Project/Laboratory_project/result/%sresult/video' % today_date).replace(' ','_')
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

def get_sv_url(url):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    findUrl = re.compile(r'<(.*?)href="(.*?)"(.*?)')
    urllist = []
    sv_url_list = []
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
            if i not in sv_url_list:   #如果链接不在二级列表中
                sv_url_list.append(i)  #添加到二级链接列表
    return sv_url_list

def get_tv_url(url):
    sv_url_list = get_sv_url(task) #找到所有二级链接
    tv_url_list = sv_url_list     #三级链接包含所有二级链接
    for sv_url in sv_url_list:    #对于每一个二级链接
        item_list = get_sv_url(sv_url) #找到对应的三级链接
        for item_url in item_list:     #对于找到的三级链接
            if item_url not in tv_url_list:   #如果不在结果列表中
                tv_url_list.append(item_url)  #添加到三级链接列表
    return tv_url_list

if __name__ == "__main__":
    task1 = ['http://www.cwa.org.cn/index.html','举重','news','2021053021','2021053021','2021053021','waiting','24','1','run','0121']
    task = ['https://search.bilibili.com/all?keyword=%E4%B8%BE%E9%87%8D&from_source=webtop_search&spm_id_from=333.788','举重','video','2021053021','2021053021','2021053021','waiting','24','2','run','0123']
    videoSpider(task)