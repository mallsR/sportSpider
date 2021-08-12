from xml.dom.minidom import parse
# dom写入和解析xml
import xml.dom.minidom

def XMLparsing(basexml):
    tasklist = []
    # 读取整个文件内容到内存并关闭文件
    DOMTree = xml.dom.minidom.parse(basexml)
    collection = DOMTree.documentElement
    # 得到所有的url
    tasklists = collection.getElementsByTagName("url")
    for task in tasklists:
        # 整理所有信息为列表
        urllist = [] 
        url = task.getAttribute('title')
        urllist.append(url)
        item = task.getElementsByTagName('item')[0].childNodes[0].data
        urllist.append(item)
        spidertype = task.getElementsByTagName('spidertype')[0].childNodes[0].data
        urllist.append(spidertype)
        starttime = task.getElementsByTagName('starttime')[0].childNodes[0].data
        urllist.append(starttime)
        endtime = task.getElementsByTagName('endtime')[0].childNodes[0].data
        urllist.append(endtime)
        runtime = task.getElementsByTagName('runtime')[0].childNodes[0].data
        urllist.append(runtime)
        state = task.getElementsByTagName('state')[0].childNodes[0].data
        urllist.append(state)
        cycle = task.getElementsByTagName('cycle')[0].childNodes[0].data
        urllist.append(cycle)
        depth = task.getElementsByTagName('depth')[0].childNodes[0].data
        urllist.append(depth)
        pstate = task.getElementsByTagName('pstate')[0].childNodes[0].data
        urllist.append(pstate)
        uid = task.getElementsByTagName('uid')[0].childNodes[0].data
        urllist.append(uid)
        tasklist.append(urllist)
    # 返回的tasklist为一个二级列表
    return tasklist