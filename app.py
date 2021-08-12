from flask import Flask,request,render_template
from flask_apscheduler import APScheduler
from mainController import main
from addtask import addtask
from changetask import changetask
from XMLparsing import XMLparsing

_basexml = "task.xml"

class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [  
        {
            'id': 'job1',
            'func': 'mainController:main',
            'args': (),
            'trigger': 'cron',
            'day': '*',
            'hour': '5',
            'minute': '41',
            'second': '50'
        }
    ]
    CHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())  # 为实例化的flask引入配置
 
 
## 
@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/add",methods=["POST","GET"])
def index1():
    _url = request.args.get("url")
    _item = request.args.get("item")
    _spidertype = request.args.get("spidertype")
    _starttime = request.args.get("starttime")
    _endtime = request.args.get("endtime")
    _cycle = request.args.get("cycle")
    _depth = request.args.get("depth")
    if _url != None and _url != "":
        addtask(_basexml, _url, _item, _spidertype, _starttime, _endtime, _cycle, _depth)
    # return "接收到表单数据是:%s"%(data)
    return render_template("add.html")

@app.route("/journal",methods=["POST","GET"])
def index2():
    return render_template("journal.html")

@app.route("/currenttask",methods=["POST","GET"])
def index3():
    _list = XMLparsing(_basexml)
    return render_template("currenttask.html",tasklist = _list)

@app.route("/details/<uid>",methods=["POST","GET"])
def index4(uid):
    _task = []
    _list = XMLparsing(_basexml)
    _url = request.args.get("url")
    _item = request.args.get("item")
    _spidertype = request.args.get("spidertype")
    _endtime = request.args.get("endtime")
    _runtime = request.args.get("runtime")
    _cycle = request.args.get("cycle")
    _depth = request.args.get("depth")
    _pstate = request.args.get("pstate")
    if _url != None and _url != "":
        changetask(_basexml, _url, _item, _spidertype, _endtime, _runtime, _cycle, _depth, _pstate, uid)
    # return "接收到表单数据是:%s"%(data)
    for stask in _list:
        if stask[10] == uid:
            _task.append(stask)
    return render_template("details.html",task = _task[0])
 
if __name__ == '__main__':
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)