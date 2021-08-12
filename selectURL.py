import datetime

def selectURL(task_list):
    updatetask_list = []
    overduetask_list = []
    today_date = int(datetime.datetime.now().strftime('%Y%m%d%H'))
    for task in task_list:
        if task[9] == 'run':
            if int(task[4]) <= today_date:
                overduetask_list.append(task)
            else:
                if int(task[5]) <= today_date:
                    task[5] = adddate(task[7])
                    updatetask_list.append(task)
                else:
                    pass
    return updatetask_list,overduetask_list

def adddate(cycle):
    delta = datetime.timedelta(hours=int(cycle))
    today_date = datetime.datetime.now()
    n_days = today_date + delta
    return n_days.strftime('%Y%m%d%H')