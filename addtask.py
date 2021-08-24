import xml.etree.ElementTree as ET
import uuid
import re

def addtask(_basexml, _url, _item, _spidertype, _starttime, _endtime, _cycle, _depth):
    # f = open(_basexml)
    # xml_text = f.read()
    # collection = ET.fromstring(xml_text)
    basetask = ET.parse(_basexml)
    collection = basetask.getroot()
    task = ET.SubElement(collection, "url")
    task.attrib = {"title":_url}
    item = ET.SubElement(task, "item")
    item.text = re.escape(_item)
    print("_item = ", _item)
    print('item.text = ', item.text)
    spidertype = ET.SubElement(task, "spidertype")
    spidertype.text = _spidertype
    starttime = ET.SubElement(task, "starttime")
    starttime.text = _starttime
    endtime = ET.SubElement(task, "endtime")
    endtime.text = _endtime
    runtime = ET.SubElement(task, "runtime")
    runtime.text = _starttime
    state = ET.SubElement(task, "state")
    state.text = "waiting"
    cycle = ET.SubElement(task, "cycle")
    cycle.text = _cycle
    depth = ET.SubElement(task, "depth")
    depth.text = _depth
    pstate = ET.SubElement(task, "pstate")
    pstate.text = "run"
    uid = ET.SubElement(task, "uid")
    uid.text = str(uuid.uuid1())
    basetask.write(_basexml, encoding = 'utf-8')
    # f.close()