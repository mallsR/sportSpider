from bs4 import BeautifulSoup
import re
import requests
import uuid
import datetime
import time
import os
import codecs
import urllib.request
import json
import xlwt
import pandas as pd



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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
    data = requests.get(baseUrl, headers = headers).json()['content']
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
        info = requests.get(url, headers= headers).json()
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
            results = requests.get(url, headers= headers).json()
            print("results = ",results)
            sheetName = results['DisciplineName']
            results = results['Heats'][0]['Results']
            # 开始写入数据
            print("result = ", results)
            # 将结果写入的excel表格
            sheet = book.add_sheet(sheetName, cell_overwrite_ok= 'true')
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
    print("跆拳道比赛信息爬取")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
        "Cookie": "cna=pRcHGW7kAHgCAXH60P4STqx8; sca=b874bf66; atpsida=6c449ef7356bd5d4a4efb49f_1629510292_4"}
    # baseUrl = "http://www.worldtaekwondo.org/competition/list.html?mcd=A01&sc=re"
    print('task[0] = ', task[0])
    html = requests.get(task[0], headers=headers)
    html.raise_for_status()
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, "html.parser")

    findInfo = re.compile(r'<span class="subj"><a href="(.*?)">(.*?)</a></span>', re.S)
    findFilePath = re.compile(r'file=(.*?)"', re.S)

    for item in soup.find_all('div', class_="result"):
        item = str(item)
        Info = re.findall(findInfo, item)
        url = "http://www.worldtaekwondo.org" + Info[0][0]
        print("url = ", url)
        path = getpath(task)
        fileName = path + '/' + Info[0][1] + '.pdf'

        # "viewer_pdf/external/pdfjs-2.1.266-dist/web/viewer.html%3Ffile=http://www.worldtaekwondo.org/att_file/news/[Result]%20Final_Online%202021%20World%20Taekwondo%20Poomsae%20Open%20Challenge%20II(WT%20Open).pdf"
        # "http://www.worldtaekwondo.org/att_file/news/[Result]%20Final_Online%202021%20World%20Taekwondo%20Poomsae%20Open%20Challenge%20II(WT%20Open).pdf"
        #                               "att_file/news/[Result]%20Final_Online%202021%20World%20Taekwondo%20Poomsae%20Open%20Challenge%20II(WT%20Open).pdf"

        data = getsoup([url])
        data = str(data)
        # print("data = ", data)
        # 可以从soup中获取文件链接
        filePath = re.findall(findFilePath, data)
        if filePath != []:
            filePath = filePath[0].replace(' ', '%20')
        # print("filePath = ", filePath)

        results = requests.get(filePath, headers=headers, stream=True)
        results.encoding = results.apparent_encoding
        with open(fileName, 'wb') as fo:
            fo.write(results.content)
    return news_num, video_num, player_num, game_num

def Boxing(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

def classicalWrestling(task, news_num, video_num, player_num, game_num):
    return news_num, video_num, player_num, game_num

# 田径基本完成
def Athletics(task, news_num, video_num, player_num, game_num):
    print("-----------------------------------Athletics---------------------------------------")
    itemName = ["Men's 60mH indoor", "Men's 60mH indoor", "Men's 100mH indoor", "Men's 200m indoor", "Men's 4x100m indoor", "Men's 4x200m indoor"]
    # 访问页面所需信息
    url = "https://qbr4c54xfjabxaeut2p2o4i6wy.appsync-api.eu-west-1.amazonaws.com/graphql"
    headers = {
        "authority": "qbr4c54xfjabxaeut2p2o4i6wy.appsync-api.eu-west-1.amazonaws.com",
        "method": "POST",
        "path": "/graphql",
        "scheme": "https",
        "x-amz-user-agent": "aws-amplify/3.0.2",
        "x-api-key": "da2-nsqt2z2ltbcnlkim6tgecikknm"
    }
    payload = {
        "operationName": "getCalendarEvents",
        "query": "query getCalendarEvents($startDate: String, $endDate: String, $query: String, $regionType: String, $regionId: Int, $disciplineId: Int, $rankingCategoryId: Int, $permitLevelId: Int, $competitionGroupId: Int, $competitionSubgroupId: Int, $competitionGroupSlug: String, $limit: Int, $offset: Int, $showOptionsWithNoHits: Boolean, $hideCompetitionsWithNoResults: Boolean, $orderDirection: OrderDirectionEnum) {\n  getCalendarEvents(startDate: $startDate, endDate: $endDate, query: $query, regionType: $regionType, regionId: $regionId, disciplineId: $disciplineId, rankingCategoryId: $rankingCategoryId, permitLevelId: $permitLevelId, competitionGroupId: $competitionGroupId, competitionSubgroupId: $competitionSubgroupId, competitionGroupSlug: $competitionGroupSlug, limit: $limit, offset: $offset, showOptionsWithNoHits: $showOptionsWithNoHits, hideCompetitionsWithNoResults: $hideCompetitionsWithNoResults, orderDirection: $orderDirection) {\n    hits\n    paginationPage\n    defaultOffset\n    options {\n      regions {\n        world {\n          id\n          name\n          count\n          __typename\n        }\n        area {\n          id\n          name\n          count\n          __typename\n        }\n        country {\n          id\n          name\n          count\n          __typename\n        }\n        __typename\n      }\n      disciplines {\n        id\n        name\n        count\n        __typename\n      }\n      rankingCategories {\n        id\n        name\n        count\n        __typename\n      }\n      disciplines {\n        id\n        name\n        count\n        __typename\n      }\n      permitLevels {\n        id\n        name\n        count\n        __typename\n      }\n      competitionGroups {\n        id\n        name\n        count\n        __typename\n      }\n      competitionSubgroups {\n        id\n        name\n        count\n        __typename\n      }\n      __typename\n    }\n    parameters {\n      startDate\n      endDate\n      query\n      regionType\n      regionId\n      disciplineId\n      rankingCategoryId\n      permitLevelId\n      competitionGroupId\n      competitionSubgroupId\n      limit\n      offset\n      showOptionsWithNoHits\n      hideCompetitionsWithNoResults\n      __typename\n    }\n    results {\n      id\n      iaafId\n      hasResults\n      hasApiResults\n      hasStartlist\n      name\n      venue\n      area\n      rankingCategory\n      disciplines\n      competitionGroup\n      competitionSubgroup\n      startDate\n      endDate\n      dateRange\n      undeterminedCompetitionPeriod {\n        status\n        label\n        remark\n        __typename\n      }\n      season\n      wasUrl\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "disciplineId": 4,
            "hideCompetitionsWithNoResults": "true",
            "isRegionTypeReset": "false",
            "isSearchReset": "false",
            "limit": 50,
            "offset": 0,
            "orderDirection": "Ascending",
            "regionType": "world",
            "showOptionsWithNoHits": "false",
            "__typename": "CalendarParams"
        }
    }
    data = requests.post(url, headers = headers, data= json.dumps(payload)).json()['data']['getCalendarEvents']['results']
    # print("data = ", data)
    # 对页面数据进行解析
    findItemName = re.compile(r'<h2>(.*?)</h2>', re.S)
    findTypeName = re.compile(r'<h1 class="styles_title__2cfb8">(.*?)<!-- --> - <!-- -->(.*?)</h1>', re.S)
    findRoundName = re.compile(r'<strong>(.*?)<!-- --> (.*?)</strong>', re.S)
    findRoundName2 = re.compile(r'<strong>(.*?)</strong>', re.S)

    path = getpath(task)
    for gameNumber in data:
        # 文件操作
        gameName = gameNumber['name']
        fileName = path + '/' + str(gameName) + '.xls'
        url = 'https://www.worldathletics.org/competition/calendar-results/results/' + str(gameNumber['id'])
        print("url = ", url)

        writer = pd.ExcelWriter(fileName)
        # # 构建sheetName
        # itemNames = []
        # soup = getsoup([url])
        # typeNames = []
        # for typeInfo in soup.find_all('h1', class_='styles_title__2cfb8'):
        #     typeName = re.findall(findTypeName, str(typeInfo))
        #     typeNames.append(str(typeName[0][0])[0:3])
        #
        # for gameInfo in soup.find_all('section', class_='EventResults_eventResult__3oyX4'):
        #     itemTitle = gameInfo.find('h2')
        #     itemName = re.findall(findItemName, str(itemTitle))
        #     itemNames.append(itemName[0])
        #
        # for i in range(len(itemNames) - len(typeNames), len(itemNames)):
        #     # excel sheetname 有格式要求
        #     itemNames[i] = (typeNames[i - (len(itemNames) - len(typeNames))] + ' ' + itemNames[i]).replace('/', ' ')[0:30]

        soup = getsoup([url])
        writeFlag = False
        typeNames = []
        for gameInfo in soup.find_all('section', class_='EventResults_eventResult__3oyX4'):
            typeName = re.findall(findItemName, str(gameInfo))[0]
            # 是否满足类型要求及去重
            if typeName not in itemName:
                continue
            if typeName in typeNames:
                continue
            typeNames.append(typeName)

            writeFlag = True
            info = pd.DataFrame()
            roundNames = []
            for gameInfoType in gameInfo.find_all('span', class_ = 'EventResults_eventMeta__75ELD'):
                roundName = re.findall(findRoundName, str(gameInfoType))
                # print("roundName = ", roundName)
                if roundName != []:
                    roundName = roundName[0]
                    roundName = pd.DataFrame([roundName[0] + ' ' + roundName[1]])
                else:
                    roundName = re.findall(findRoundName2, str(gameInfoType))[0]
                    roundName = pd.DataFrame([roundName])
                roundNames.append(roundName)

            index = 0
            for athInfo in pd.read_html(gameInfo.prettify()):
                info = pd.concat([info, roundNames[index]])
                index += 1
                info = pd.concat([info, athInfo])
            info = info[[0, 'Place', 'Name', 'Birth Date', 'Nat.', 'Mark']]
            info.to_excel(writer, sheet_name=typeName)
        if writeFlag == True:
            writer.save()
            writer.close()

    return news_num, video_num, player_num, game_num

# 跳远基本完成，重复名进行简单过滤
def longJumping(task, news_num, video_num, player_num, game_num):
    print("----------------------------------longJumping---------------------------------------")
    itemName = ["Men's Long Jump indoor", "Men's Triple Jump indoor"]
    # 访问页面所需信息
    url = "https://qbr4c54xfjabxaeut2p2o4i6wy.appsync-api.eu-west-1.amazonaws.com/graphql"
    headers = {
        "authority": "qbr4c54xfjabxaeut2p2o4i6wy.appsync-api.eu-west-1.amazonaws.com",
        "method": "POST",
        "path": "/graphql",
        "scheme": "https",
        "x-amz-user-agent": "aws-amplify/3.0.2",
        "x-api-key": "da2-nsqt2z2ltbcnlkim6tgecikknm"
    }
    payload = {
        "operationName": "getCalendarEvents",
        "query": "query getCalendarEvents($startDate: String, $endDate: String, $query: String, $regionType: String, $regionId: Int, $disciplineId: Int, $rankingCategoryId: Int, $permitLevelId: Int, $competitionGroupId: Int, $competitionSubgroupId: Int, $competitionGroupSlug: String, $limit: Int, $offset: Int, $showOptionsWithNoHits: Boolean, $hideCompetitionsWithNoResults: Boolean, $orderDirection: OrderDirectionEnum) {\n  getCalendarEvents(startDate: $startDate, endDate: $endDate, query: $query, regionType: $regionType, regionId: $regionId, disciplineId: $disciplineId, rankingCategoryId: $rankingCategoryId, permitLevelId: $permitLevelId, competitionGroupId: $competitionGroupId, competitionSubgroupId: $competitionSubgroupId, competitionGroupSlug: $competitionGroupSlug, limit: $limit, offset: $offset, showOptionsWithNoHits: $showOptionsWithNoHits, hideCompetitionsWithNoResults: $hideCompetitionsWithNoResults, orderDirection: $orderDirection) {\n    hits\n    paginationPage\n    defaultOffset\n    options {\n      regions {\n        world {\n          id\n          name\n          count\n          __typename\n        }\n        area {\n          id\n          name\n          count\n          __typename\n        }\n        country {\n          id\n          name\n          count\n          __typename\n        }\n        __typename\n      }\n      disciplines {\n        id\n        name\n        count\n        __typename\n      }\n      rankingCategories {\n        id\n        name\n        count\n        __typename\n      }\n      disciplines {\n        id\n        name\n        count\n        __typename\n      }\n      permitLevels {\n        id\n        name\n        count\n        __typename\n      }\n      competitionGroups {\n        id\n        name\n        count\n        __typename\n      }\n      competitionSubgroups {\n        id\n        name\n        count\n        __typename\n      }\n      __typename\n    }\n    parameters {\n      startDate\n      endDate\n      query\n      regionType\n      regionId\n      disciplineId\n      rankingCategoryId\n      permitLevelId\n      competitionGroupId\n      competitionSubgroupId\n      limit\n      offset\n      showOptionsWithNoHits\n      hideCompetitionsWithNoResults\n      __typename\n    }\n    results {\n      id\n      iaafId\n      hasResults\n      hasApiResults\n      hasStartlist\n      name\n      venue\n      area\n      rankingCategory\n      disciplines\n      competitionGroup\n      competitionSubgroup\n      startDate\n      endDate\n      dateRange\n      undeterminedCompetitionPeriod {\n        status\n        label\n        remark\n        __typename\n      }\n      season\n      wasUrl\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "disciplineId": 4,
            "hideCompetitionsWithNoResults": "true",
            "isRegionTypeReset": "false",
            "isSearchReset": "false",
            "limit": 50,
            "offset": 0,
            "orderDirection": "Ascending",
            "regionType": "world",
            "showOptionsWithNoHits": "false",
            "__typename": "CalendarParams"
        }
    }
    data = requests.post(url, headers=headers, data=json.dumps(payload)).json()['data']['getCalendarEvents']['results']
    print("data = ", data)
    # 对页面数据进行解析
    findItemName = re.compile(r'<h2>(.*?)</h2>', re.S)
    findTypeName = re.compile(r'<h1 class="styles_title__2cfb8">(.*?)<!-- --> - <!-- -->(.*?)</h1>', re.S)

    path = getpath(task)
    for gameNumber in data:
        # 文件操作
        gameName = gameNumber['name']
        fileName = path + '/' + str(gameName) + '.xls'
        url = 'https://www.worldathletics.org/competition/calendar-results/results/' + str(gameNumber['id'])
        print("url = ", url)

        writer = pd.ExcelWriter(fileName)
        # # 构建sheetName
        # itemNames = []
        # soup = getsoup([url])
        # typeNames = []
        # for typeInfo in soup.find_all('h1', class_='styles_title__2cfb8'):
        #     typeName = re.findall(findTypeName, str(typeInfo))
        #     typeNames.append(str(typeName[0][0])[0:3])
        #
        # for gameInfo in soup.find_all('section', class_='EventResults_eventResult__3oyX4'):
        #     itemTitle = gameInfo.find('h2')
        #     itemName = re.findall(findItemName, str(itemTitle))
        #     itemNames.append(itemName[0])
        #
        # for i in range(len(itemNames) - len(typeNames), len(itemNames)):
        #     # excel sheetname 有格式要求
        #     itemNames[i] = (typeNames[i - (len(itemNames) - len(typeNames))] + ' ' + itemNames[i]).replace('/', ' ')[0:30]

        soup = getsoup([url])
        writeFlag = False
        typeNames = []
        for gameInfo in soup.find_all('section', class_ = 'EventResults_eventResult__3oyX4'):
            typeName = re.findall(findItemName, str(gameInfo))[0]
            if typeName not in itemName:
                continue
            if typeName in typeNames:
                continue
            typeNames.append(typeName)

            writeFlag = True
            info = pd.DataFrame()
            for athInfo in pd.read_html(gameInfo.prettify()):
                info = pd.concat([info, athInfo])
            info.to_excel(writer, sheet_name = typeName)
        if writeFlag == True:
            writer.save()
            writer.close()


    return news_num, video_num, player_num, game_num


# 竞走比赛信息爬取，基本完成
def raceWalking(task, news_num, video_num, player_num, game_num):
    path = getpath(task)
    url = "https://qbr4c54xfjabxaeut2p2o4i6wy.appsync-api.eu-west-1.amazonaws.com/graphql"
    headers = {
        "authority":"qbr4c54xfjabxaeut2p2o4i6wy.appsync-api.eu-west-1.amazonaws.com",
        "method":"POST",
        "path":"/graphql",
        "scheme":"https",
        "x-amz-user-agent":"aws-amplify/3.0.2",
        "x-api-key":"da2-nsqt2z2ltbcnlkim6tgecikknm"
    }
    payload = {
        "operationName": "getCalendarEvents",
        "query": "query getCalendarEvents($startDate: String, $endDate: String, $query: String, $regionType: String, $regionId: Int, $disciplineId: Int, $rankingCategoryId: Int, $permitLevelId: Int, $competitionGroupId: Int, $competitionSubgroupId: Int, $competitionGroupSlug: String, $limit: Int, $offset: Int, $showOptionsWithNoHits: Boolean, $hideCompetitionsWithNoResults: Boolean, $orderDirection: OrderDirectionEnum) {\n  getCalendarEvents(startDate: $startDate, endDate: $endDate, query: $query, regionType: $regionType, regionId: $regionId, disciplineId: $disciplineId, rankingCategoryId: $rankingCategoryId, permitLevelId: $permitLevelId, competitionGroupId: $competitionGroupId, competitionSubgroupId: $competitionSubgroupId, competitionGroupSlug: $competitionGroupSlug, limit: $limit, offset: $offset, showOptionsWithNoHits: $showOptionsWithNoHits, hideCompetitionsWithNoResults: $hideCompetitionsWithNoResults, orderDirection: $orderDirection) {\n    hits\n    paginationPage\n    defaultOffset\n    options {\n      regions {\n        world {\n          id\n          name\n          count\n          __typename\n        }\n        area {\n          id\n          name\n          count\n          __typename\n        }\n        country {\n          id\n          name\n          count\n          __typename\n        }\n        __typename\n      }\n      disciplines {\n        id\n        name\n        count\n        __typename\n      }\n      rankingCategories {\n        id\n        name\n        count\n        __typename\n      }\n      disciplines {\n        id\n        name\n        count\n        __typename\n      }\n      permitLevels {\n        id\n        name\n        count\n        __typename\n      }\n      competitionGroups {\n        id\n        name\n        count\n        __typename\n      }\n      competitionSubgroups {\n        id\n        name\n        count\n        __typename\n      }\n      __typename\n    }\n    parameters {\n      startDate\n      endDate\n      query\n      regionType\n      regionId\n      disciplineId\n      rankingCategoryId\n      permitLevelId\n      competitionGroupId\n      competitionSubgroupId\n      limit\n      offset\n      showOptionsWithNoHits\n      hideCompetitionsWithNoResults\n      __typename\n    }\n    results {\n      id\n      iaafId\n      hasResults\n      hasApiResults\n      hasStartlist\n      name\n      venue\n      area\n      rankingCategory\n      disciplines\n      competitionGroup\n      competitionSubgroup\n      startDate\n      endDate\n      dateRange\n      undeterminedCompetitionPeriod {\n        status\n        label\n        remark\n        __typename\n      }\n      season\n      wasUrl\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "disciplineId": 3,
            "hideCompetitionsWithNoResults": "true",
            "isRegionTypeReset": "false",
            "isSearchReset": "false",
            "limit": 50,
            "offset": 0,
            "orderDirection": "Ascending",
            "regionType": "world",
            "showOptionsWithNoHits": "false",
            "__typename": "CalendarParams"
        }
    }
    data = requests.post(url, headers = headers, data = json.dumps(payload)).json()['data']['getCalendarEvents']['results']

    # 正则表达式，匹配内容
    findItemName = re.compile(r'<h2>(.*?)</h2>', re.S)
    findTypeName = re.compile(r'<h1 class="styles_title__2cfb8">(.*?)<!-- --> - <!-- -->(.*?)</h1>', re.S)

    for gameNumber in data:
        # 文件操作
        gameName = gameNumber['name']
        fileName = path + '/' + str(gameName) + '.xls'

        url = 'https://www.worldathletics.org/competition/calendar-results/results/' + str(gameNumber['id'])
        # 获取数据
        writer = pd.ExcelWriter(fileName)
        # 构建sheetName
        itemNames = []
        soup = getsoup([url])
        typeNames = []
        for typeInfo in soup.find_all('h1', class_ = 'styles_title__2cfb8'):
            typeName = re.findall(findTypeName, str(typeInfo))
            typeNames.append(str(typeName[0][0])[0:3])

        for gameInfo in soup.find_all('section', class_ = 'EventResults_eventResult__3oyX4'):
            itemTitle = gameInfo.find('h2')
            itemName = re.findall(findItemName, str(itemTitle))
            itemNames.append(itemName[0])

        for i in range(len(itemNames) - len(typeNames), len(itemNames)):
            # excel sheetname 有格式要求
            itemNames[i] = (typeNames[i - (len(itemNames) - len(typeNames))] + ' ' + itemNames[i]).replace('/', ' ')[0:30]


        index = 0
        for gameInfo in soup.find_all('section', class_='EventResults_eventResult__3oyX4'):
            athInfo = pd.read_html(gameInfo.prettify())[0]
            athInfo.to_excel(writer, sheet_name= itemNames[index])
            index += 1

        writer.save()
        writer.close()


    return news_num, video_num, player_num, game_num

# 举重比赛的爬取，基本完成
def weightLifting(task, news_num, video_num, player_num, game_num):
    soup = getsoup(task)
    path = getpath(task)
    print("path = ", path)
    # print("soup = ", soup)
    findEventID = re.compile(r'href="(.*?)"', re.S)
    findEventName = re.compile(r'<span class="text">(.*?)</span>', re.S)

    findSheetName = re.compile(r'<h2>(.*?)n</h2>', re.S)

    # 找运动员信息的正则
    findAthleteName = re.compile(r'<div class="col-7 not__cell__767">\s<p>\s(.*?)</p>', re.S)
    findNation = re.compile(r'<span class="flag"><img alt="(.*?)" src="(.*?)"/></span>', re.S)
    findBorn = re.compile(r'Born: </span>(.*?)\s</p>', re.S)
    findWeight = re.compile(r'B.weight: </span>(\d+(\.\d+)?)\s</p>', re.S)
    findGroup = re.compile(r'Group: </span>(.)\s</p>', re.S)
    findSnatch = re.compile(r'Snatch: </span><strong>(\d+)</strong>\s</p>', re.S)
    findCIJerk = re.compile(r'CI&amp;Jerk: </span><strong>(\d+)</strong>\s</p>', re.S)
    findTotal = re.compile(r'<strong><span class="only__mobile">Total: </span>(\d+)</strong>', re.S)

    for item in soup.find_all('a', class_ = "card"):
        item = str(item)
        eventID = re.findall(findEventID, item)
        print("eventID = ", eventID)

        # 设置文件信息
        eventName = re.findall(findEventName, item)
        fileName = path + '/' + str(eventName[0]) + '.xls'
        print("fileName = ", fileName)
        colName = ['Rank', 'Name', 'Nation', 'Born', 'B.weight', 'Group', 'Snatch', 'CI&Jerk', 'Total']

        url = 'https://iwf.sport/results/results-by-events/' + eventID[0]
        print("url = ", url)
        info = getsoup([url])
        # print("info = ", info)

        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        row = 0
        # 男子成绩
        sheet = book.add_sheet("Men's Total", cell_overwrite_ok= 'true')
        for itemInfo in info.find_all('div', id = "men_total"):
            # 获取项目名
            sheetNames = []
            index = 0
            for itemName in itemInfo.find_all('div', class_='results__title'):
                itemName = str(itemName)
                sheetName = re.findall(findSheetName, itemName)
                sheetNames.append(sheetName[0])
            print("sheetNames = ", sheetNames)

            for itemData in itemInfo.find_all('div',  class_ = 'cards'):
                # itemData = str(itemData)
                # print("itemData = ", itemData)
                # 先写入项目名
                sheet.write(row, 0, sheetNames[index])
                row += 1
                index += 1
                # 再写入列名
                for i in range(len(colName)):
                    sheet.write(row, i, colName[i])
                # 写入运动员成绩
                row += 1
                rank = 1
                # 两个标签无法分开，需要去除第一个
                flag = 1
                for AthleteInfo in itemData.find_all('div', class_ = 'card'):
                    if flag == 1:
                        flag = 0
                        continue
                    AthleteInfo = str(AthleteInfo)
                    # print("AthleteInfo = ", AthleteInfo)
                    athleteName = re.findall(findAthleteName, AthleteInfo)
                    if athleteName != []:
                        athleteName = athleteName[0]
                    else:
                        athleteName = ''

                    nation = re.findall(findNation, AthleteInfo)
                    if nation != []:
                        nation = nation[0][0]
                    else:
                        nation = ''

                    born = re.findall(findBorn, AthleteInfo)
                    if born != []:
                        born = born[0]
                    else:
                        born = ''

                    weight = re.findall(findWeight, AthleteInfo)
                    print("weight = ", weight)
                    if weight != []:
                        weight = weight[0]
                    else:
                        weight = ''

                    group = re.findall(findGroup, AthleteInfo)
                    print("group = ", group)
                    if group != []:
                        group = group[0]
                    else:
                        group = ''

                    snatch = re.findall(findSnatch, AthleteInfo)
                    if snatch != []:
                        snatch = snatch[0]
                    else:
                        snatch = ''

                    CIJerk = re.findall(findCIJerk, AthleteInfo)
                    if CIJerk != []:
                        CIJerk = CIJerk[0]
                    else:
                        CIJerk = ''

                    total = re.findall(findTotal, AthleteInfo)
                    if total != []:
                        total = total[0]
                    else:
                        total = ''
                    infos = [rank, athleteName, nation, born, weight, group, snatch, CIJerk, total]
                    print("infos = ", infos)
                    for col in range(len(infos)):
                        sheet.write(row, col, infos[col])
                    rank += 1
                    row += 1

                # 写入成绩之后，再添加空格
                row += 1

        row = 0
        # 女子成绩
        sheet = book.add_sheet("Woen's Total", cell_overwrite_ok='true')
        for itemInfo in info.find_all('div', id="women_total"):
            # 获取项目名
            sheetNames = []
            index = 0
            for itemName in itemInfo.find_all('div', class_='results__title'):
                itemName = str(itemName)
                sheetName = re.findall(findSheetName, itemName)
                sheetNames.append(sheetName[0])
            print("sheetNames = ", sheetNames)

            for itemData in itemInfo.find_all('div', class_='cards'):
                # itemData = str(itemData)
                # print("itemData = ", itemData)
                # 先写入项目名
                sheet.write(row, 0, sheetNames[index])
                row += 1
                index += 1
                # 再写入列名
                for i in range(len(colName)):
                    sheet.write(row, i, colName[i])
                # 写入运动员成绩
                row += 1
                rank = 1
                # 两个标签无法分开，需要去除第一个
                flag = 1
                for AthleteInfo in itemData.find_all('div', class_='card'):
                    if flag == 1:
                        flag = 0
                        continue
                    AthleteInfo = str(AthleteInfo)
                    # print("AthleteInfo = ", AthleteInfo)
                    athleteName = re.findall(findAthleteName, AthleteInfo)
                    if athleteName != []:
                        athleteName = athleteName[0]
                    else:
                        athleteName = ''

                    nation = re.findall(findNation, AthleteInfo)
                    if nation != []:
                        nation = nation[0][0]
                    else:
                        nation = ''

                    born = re.findall(findBorn, AthleteInfo)
                    if born != []:
                        born = born[0]
                    else:
                        born = ''

                    weight = re.findall(findWeight, AthleteInfo)
                    print("weight = ", weight)
                    if weight != []:
                        weight = weight[0]
                    else:
                        weight = ''

                    group = re.findall(findGroup, AthleteInfo)
                    print("group = ", group)
                    if group != []:
                        group = group[0]
                    else:
                        group = ''

                    snatch = re.findall(findSnatch, AthleteInfo)
                    if snatch != []:
                        snatch = snatch[0]
                    else:
                        snatch = ''

                    CIJerk = re.findall(findCIJerk, AthleteInfo)
                    if CIJerk != []:
                        CIJerk = CIJerk[0]
                    else:
                        CIJerk = ''

                    total = re.findall(findTotal, AthleteInfo)
                    if total != []:
                        total = total[0]
                    else:
                        total = ''
                    infos = [rank, athleteName, nation, born, weight, group, snatch, CIJerk, total]
                    print("infos = ", infos)
                    for col in range(len(infos)):
                        sheet.write(row, col, infos[col])
                    rank += 1
                    row += 1

                # 写入成绩之后，再添加空格
                row += 1

        book.save(fileName)

        time.sleep(7)



    return news_num, video_num, player_num, game_num

# 散打比赛的爬取，如何加快速度
def sanda(task, news_num, video_num, player_num, game_num):
    print("-----------------------------------sanda---------------------------------------")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
        "Cookie": "cna=pRcHGW7kAHgCAXH60P4STqx8; sca=b874bf66; atpsida=6c449ef7356bd5d4a4efb49f_1629510292_4"}
    soup = getsoup(task)
    # print("soup = ", str(soup))
    path = getpath(task)

    # 正则表达式
    findGameUrl = re.compile(r'<a class="btn btn-link" href="(.*?)" target="_blank">点击下载</a>', re.S)
    findGameName = re.compile(r'<strong>(.*?)</strong>', re.S)

    for gameFile in soup.find_all('tr', class_ = 'tbody'):
        # print("gameFile = ", str(gameFile))
        gameUrl = re.findall(findGameUrl, str(gameFile))
        if gameUrl != []:
            gameUrl = gameUrl[0]
        else:
            print("Don't find url.")
        print("url = ", gameUrl)
        gameName = re.findall(findGameName, str(gameFile))
        if gameName != []:
            gameName = gameName[0]
        else:
            print("Don't find gameName")
        print("gameName = ", gameName)

        fileName = path + '/' + gameName + '.pdf'

        results = requests.get(gameUrl, headers= headers, stream = True)
        results.encoding = results.apparent_encoding
        with open(fileName, 'wb') as fo:
            fo.write(results.content)

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
    '跳远':   longJumping,
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