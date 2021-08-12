from XMLparsing import XMLparsing
from selectURL import selectURL
from playerSpider import player1Spider,player2Spider,player3Spider
from gameSpider import game1Spider
from videoSpider import videoSpider
from newsSpider import newsSpider
from updateURL import updateURL
from generatepage import generatePage
from generatelog import generateLog
from changexml import change_a,change_r
import datetime
import time

spidertypedict = {
    'player1':player1Spider,
    'player2':player2Spider,
    'player3':player3Spider,
    'game1':game1Spider,
    'video':videoSpider,
    'news':newsSpider
}

def Default(task, news_num, video_num, player_num, game_num):
    print('类型错误！')

def classifySpider(task, news_num, video_num, player_num, game_num):
    fun = spidertypedict.get(task[2],Default)
    return fun(task, news_num, video_num, player_num, game_num)

def main():
    # 解析xml文件
    news_num = 0
    video_num = 0
    player_num = 0
    game_num = 0
    task_ID = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    result_path = datetime.datetime.now().strftime('%Y-%m-%d %H')
    S_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 需要使用绝对路径
    xml_name = "/Users/xiaor/Project/Laboratory_project/program/task.xml"
    # 从xml中获取爬取任务
    task_list = XMLparsing(xml_name) 
    # 对任务分类
    updatetask_list,overduetask_list = selectURL(task_list)
    #更新列表中下次运行时间为当前时间+周期，删除列表中为需要删除的任务
    # 爬虫程序开始
    # 修改XML中运行任务的状态为running
    change_r(xml_name, updatetask_list)
    # 执行所有爬虫任务
    for task in updatetask_list:
        news_num, video_num, player_num, game_num = classifySpider(task, news_num, video_num, player_num, game_num)
    # 修改XML中运行任务的下次运行时间和任务的状态
    updateURL(xml_name, updatetask_list)
    # 修改XML中过期任务的状态为abandoned
    change_a(xml_name, overduetask_list)

    E_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 生成任务日志
    generateLog(task_ID, S_time, E_time, updatetask_list, news_num, video_num, player_num, game_num)
    #将结果存成HTML文档
    generatePage(result_path, S_time, news_num, video_num, player_num, game_num)


if __name__ == "__main__":
    main()