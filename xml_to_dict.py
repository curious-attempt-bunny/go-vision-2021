# credit: https://github.com/xthehatterx/xml_to_dict/blob/master/xml_to_dict/xml_to_dict.py

import xml.etree.ElementTree as ET, re
from collections import defaultdict
from typing import Union

class XMLtoDict(object):

    @classmethod
    def parse(cls, xml: str):
        return cls.__to_dict(ET.fromstring(xml))
    
    @classmethod
    def value_from_nest(cls, pattern: str, nest: Union[dict, str]):
        nest = nest if type(nest) is dict else cls.parse(nest)
        for k, v in nest.items():
            match = re.search(pattern, k)
            if match:
                return v
            else:
                if type(v) is dict:
                    return cls.value_from_nest(pattern, v)

    @classmethod
    def __to_dict(cls, t: str):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(cls.__to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d