import json
from .. import cache

URL_APACHE = "https://raw.githubusercontent.com/jshttp/mime-db/refs/heads/master/src/apache-types.json"
LOCAL_APACHE_JSON = "data/apache_types.json"
LOCAL_APACHE_META = "data/apache_types.meta" 
_apache_types = None


def parse_apache_json(json_path):
    global _apache_types
    if _apache_types is not None:
        return _apache_types
    items = []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for mimetype in data.keys():
            extensions = data[mimetype].get("extensions", None)
            if not extensions:
                continue
            items.append({
                "extensions": extensions,
                "type": mimetype,
                "description": None,
                "mimetype": mimetype, 
                "source": "apache",
                "source_url": None,
            })
    _iana_types = items
    return items


def load():
    cache.fetch_if_updated(URL_APACHE, LOCAL_APACHE_JSON, LOCAL_APACHE_META)
    return True

def types():
    return parse_apache_json(LOCAL_APACHE_JSON)
