from bs4 import BeautifulSoup
import re
import requests
import uuid
import datetime
import os
import codecs
import urllib.request
import json
import xlwt



def Default(task, news_num, video_num, player_num, game_num):
    print('类型错误！')

def gameSpider(task, news_num, video_num, player_num, game_num):
    fun = gameType.get(task[1], Default)
    return fun(task, news_num, video_num, player_num, game_num)

#   跳水比赛
def divingSpider(task, news_num, video_num, player_num, game_num):
    # 跳水比赛的基本形式，只需要更改时间
    baseUrl = "https://api.fina.org/fina/competitions?pageSize=100&venueDateFrom=2021-01-01T00%3A00%3A00%2B00%3A00&venueDateTo=2022-01-01T00%3A00%3A00%2B00%3A00&disciplines=DV&group=FINA&sort=dateFrom%2Casc&page=0"
    path = getpath(task)
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    data = requests.get(baseUrl, headers = head).json()['content']
    print("data = ", data)
    gameChecked = []
    for item in data:
        # 先判断比赛是否取消，通过metadata是否包含customStatus: "Cancelled"来确定
        if 'customStatus' in item['metadata'].keys() and item['metadata']['customStatus'].upper() == "CANCELLED":
            continue;
        # 比赛未被取消，判断是否举行
        date = item['dateTo'][0:10]
        print("date = ", date)
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        todayDate = datetime.datetime.now()
        if date > todayDate:
            continue;

        # 需要收集结果
        # 构造二级链接

        url = "https://api.fina.org/fina/competitions" + '/' + str(item['id']) + '/' + "events"
        # url = url.replace(' ', '-').lower()
        print("url = ", url)
        # 访问二级页面
        info = requests.get(url, headers= head).json()
        orderIndex = ''
        if info['Series'] != []:
            orderIndex = ' Leg' + str(info['Series'][0]['SeriesOrderValue'])

        # 已举行，判断是否已经收集过结果
        gameName = item['officialName'] + orderIndex
        if gameName in gameChecked:
            continue;
        gameChecked.append(gameName)
        print("gameName = ", gameName)

        fileName = path + '/' + info['Name'] + orderIndex + '.xls'
        print("fileName = ", fileName)
        info = info['Sports'][0]['DisciplineList']
        print("info = ", info)
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 构建三级结果页面链接
        for thirdItem in info:
            url = "https://api.fina.org/fina/events/" + thirdItem['Id']
            print('url = ', url)
            results = requests.get(url, headers= head).json()
            print("results = ",results)
            sheetName = results['DisciplineName']
            results = results['Heats'][0]['Results']
            # 开始写入数据
            print("result = ", results)
            # 将结果写入的excel表格
            sheet = book.add_sheet(sheetName, cell_overwrite_ok= True)
            col = ['Rank', 'Country', 'Athlete', 'Age', 'Points', 'Pts Behind']
            for i in range(len(col)):
                sheet.write(0, i, col[i])
            dataName = ['Rank', 'NAT', 'FullName', 'AthleteResultAge', 'TotalPoints', 'PointsBehind']
            rank = 1
            for i in range(len(results)):
                sheet.write(i, 0, rank)
                rank = rank + 1
                for j in range(1, len(col)):
                    # 需要对年龄这里进行额外的处理
                    # print("j = %s, results[%d].keys()" % (j, i , results[i].keys()))
                    if j != 3 or 'AthleteResultAge' in results[i].keys():
                        sheet.write(i + 1, j, results[i][dataName[j]])
                    else:
                        # print("results[i].keys() = ", results[i].keys())
                        print("results[i]['Competitors'] = ", results[i]['Competitors'])
                        if results[i]['Competitors'] != None:
                            age = str(results[i]['Competitors'][0]['AthleteResultAge']) + '/' + str(results[i]['Competitors'][1]['AthleteResultAge'])
                            sheet.write(i + 1, j, age)
                        else:
                            sheet.write(i + 1, j, '')

        book.save(fileName)
    return news_num, video_num, player_num, game_num

# 跆拳道
def Taekwondo(task, news_num, video_num, player_num, game_num):
    
    return news_num, video_num, player_num, game_num

def Boxing(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def classicalWrestling(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def Athletics(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def raceWalking(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def broadJumping(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def weightLifting(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def sanda(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def freedom(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

gameType = {
    '跳水': divingSpider,
    '跆拳道': Taekwondo,
    '拳击':  Boxing,
    '古典跤': classicalWrestling,
    '田径':   Athletics,
    '竞走':   raceWalking,
    '跳远':   broadJumping,
    '举重':   weightLifting,
    '武术散打': sanda,
    '自由跤':  freedom
}

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
    f = open("%s/%s.jpg"%(path, file_name),'wb')
    f.write(urllib.request.urlopen(requesti).read())
    f.close()

def getpath(task):
    today_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H'))
    path = ('/Users/xiaor/Project/Laboratory_project/result/%sresult/%s/game' % (today_date, task[1])).replace(' ', '_')
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return path

if __name__ == "__main__":
    task = ['https://new.qq.com/omn/20210418/20210418A01F8I00.html']
    game1Spider(task)