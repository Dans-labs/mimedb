import os
import xml.etree.ElementTree as ET
from .. import cache

URL = "https://raw.githubusercontent.com/galaxyproject/galaxy/refs/heads/dev/lib/galaxy/config/sample/datatypes_conf.xml.sample"
LOCAL_XML = "data/galaxy_types.xml"
LOCAL_META = "data/galaxy_types.meta"  # stores ETag and Last-Modified

def parse_datatypes(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    extracted = []
    for dt in root.findall(".//datatype"):
        extracted.append({
            "extensions": [dt.get("extension")],
            "type": dt.get("type"),
            "description": dt.get("description"),
            "mimetype": dt.get("mimetype"),
            "source": "galaxy",
            "source_url": None,
        })

    return extracted

def load():
    cache.fetch_if_updated(URL, LOCAL_XML, LOCAL_META)
    return True

def types():
    if os.path.exists(LOCAL_XML):
        return parse_datatypes(LOCAL_XML)
    else:
        load()
        return parse_datatypes(LOCAL_XML)

