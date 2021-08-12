import xml.etree.ElementTree as ET

def changetask(_basexml, _url, _item, _spidertype, _endtime, _runtime, _cycle, _depth, _pstate, uid):
    basetask = ET.parse(_basexml)
    collection = basetask.getroot()
    for urlnode in collection.findall("url"):
        if urlnode.find('uid').text == uid:
            # urlnode.find('url').text = _url
            urlnode.find('item').text = _item
            urlnode.find('spidertype').text = _spidertype
            urlnode.find('endtime').text = _endtime
            urlnode.find('runtime').text = _runtime
            urlnode.find('cycle').text = _cycle
            urlnode.find('depth').text = _depth
            urlnode.find('pstate').text = _pstate
    basetask.write(_basexml)