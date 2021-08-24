# 处理xml
import xml.etree.ElementTree as ET

def change_r(xml_name, task_list):
    basetask = ET.parse(xml_name)
    collection = basetask.getroot()
    for urlnode in collection.findall("url"):
        for task in task_list:
            if urlnode.find('uid').text == task[10]:
                urlnode.find('state').text = 'running'
    basetask.write(xml_name, encoding = 'utf-8')

def change_a(xml_name, task_list):
    basetask = ET.parse(xml_name)
    collection = basetask.getroot()
    for urlnode in collection.findall("url"):
        for task in task_list:
            if urlnode.find('uid').text == task[10]:
                urlnode.find('state').text = 'abandoned'
                task_list.remove(task)
    basetask.write(xml_name)