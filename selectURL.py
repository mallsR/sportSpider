import datetime

def selectURL(task_list):
    updatetask_list = []
    overduetask_list = []
    # strftime 格式化时间
    today_date = int(datetime.datetime.now().strftime('%Y%m%d%H'))
    for task in task_list:
        if task[9] == 'run':
            # 结束时间小于现在的时间，证明过期
            if int(task[4]) <= today_date:
                overduetask_list.append(task)
            else:
                # 运行时间小于现在的时间
                if int(task[5]) <= today_date:
                    task[5] = adddate(task[7])
                    updatetask_list.append(task)
                else:
                    pass
    # 两个任务均为二级列表
    return updatetask_list,overduetask_list

def adddate(cycle):
    delta = datetime.timedelta(hours=int(cycle))
    today_date = datetime.datetime.now()
    n_days = today_date + delta
    return n_days.strftime('%Y%m%d%H')