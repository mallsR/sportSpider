import xml.etree.ElementTree as ET
import uuid

def addtask(_basexml, _url, _item, _spidertype, _starttime, _endtime, _cycle, _depth):
    basetask = ET.parse(_basexml)
    collection = basetask.getroot()
    task = ET.SubElement(collection, "url")
    task.attrib = {"title":_url}
    item = ET.SubElement(task, "item")
    item.text = _item
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
    basetask.write(_basexml)