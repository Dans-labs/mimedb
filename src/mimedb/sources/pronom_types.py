import re
import requests
from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET
from .. import cache

BASE_URL = "https://www.nationalarchives.gov.uk/aboutapps/pronom/droid-signature-files.htm"
LOCAL_XML = "data/pronom_types.xml"
LOCAL_META = "data/pronom_types.meta"  # stores ETag and Last-Modified


def get_latest_version(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    versions = []

    for link in soup.find_all("a"):
        href = link.get("href", "")
        m = re.search(r"DROID_SignatureFile_V(\d+)\.xml", href)
        if m:
            versions.append((int(m.group(1)), href))

    latest_version, latest_url = max(versions)

    # print("Latest version:", latest_version)
    # print("URL:", latest_url)

    return latest_url

def parse_datatypes(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    extracted = []
    for dt in root.findall(".//{*}FileFormat"):
        name = dt.get("Name")
        mimetype  = dt.get("MIMEType")
        ext_elem = dt.find("{*}Extension")
        ext = ext_elem.text if ext_elem is not None else None
        if not ext or not mimetype:
            continue
        extracted.append({
            "extensions": [ext] if ext else [],
            "type": mimetype,
            "description": name,
            "mimetype": mimetype,
            "source": "pronom",
            "source_url": None,
        })

    return extracted

def load():
    URL = get_latest_version(BASE_URL)
    cache.fetch_if_updated(URL, LOCAL_XML, LOCAL_META)
    return True

def types():
    if os.path.exists(LOCAL_XML):
        return parse_datatypes(LOCAL_XML)
    else:
        load()
        return parse_datatypes(LOCAL_XML)

