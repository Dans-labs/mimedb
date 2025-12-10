import csv
import json
from .. import cache


URL_IANA = "https://raw.githubusercontent.com/jshttp/mime-db/refs/heads/master/src/iana-types.json"
LOCAL_IANA_JSON = "data/iana_types.json"
LOCAL_IANA_META = "data/iana_types.meta"  
IANA_BASE_URL = "https://www.iana.org/assignments/media-types/"

_iana_types = None

def parse_iana_json(json_path):
    global _iana_types
    if _iana_types is not None:
        return _iana_types
    items = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for mimetype in data.keys():
            extensions = data[mimetype].get("extensions", None)
            if not extensions:
                continue
            # apache_record = _apache_types.get(mimetype, {})
            # if not apache_record:
            #     continue
            items.append({
                "extensions": extensions,
                "type": mimetype,
                "description": None,
                "mimetype": mimetype, 
                "source": "iana",
                "source_url": IANA_BASE_URL + mimetype,
            })
    _iana_types = items
    return items

def load():
    cache.fetch_if_updated(URL_IANA, LOCAL_IANA_JSON, LOCAL_IANA_META)
    return True

def types():
    return parse_iana_json(LOCAL_IANA_JSON)
