import xml.etree.ElementTree as ET

def updateURL(xml_name, task_list):
    basetask = ET.parse(xml_name)
    collection = basetask.getroot()
    for urlnode in collection.findall("url"):
        for task in task_list:
            if urlnode.find('uid').text == task[10]:
                urlnode.find('runtime').text = task[5]
                urlnode.find('state').text = 'waiting'
    basetask.write(xml_name)