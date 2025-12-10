import os
import requests

def load_local_metadata(local_meta_path):
    if not os.path.exists(local_meta_path):
        return {}
    meta = {}
    with open(local_meta_path, "r") as f:
        for line in f:
            k, v = line.strip().split("=", 1)
            meta[k] = v
    return meta


def save_local_metadata(local_meta_path, etag, last_modified):
    with open(local_meta_path, "w") as f:
        if etag:
            f.write(f"ETag={etag}\n")
        if last_modified:
            f.write(f"LastModified={last_modified}\n")


def fetch_if_updated(url, local_data_path, local_meta_path):
    headers = {}
    meta = load_local_metadata(local_meta_path)

    # Conditional GET headers
    if "ETag" in meta:
        headers["If-None-Match"] = meta["ETag"]
    if "LastModified" in meta:
        headers["If-Modified-Since"] = meta["LastModified"]

    # print("Checking for updates…")
    resp = requests.get(url, headers=headers)

    if resp.status_code == 304:
        # print("✔ Local copy is up to date.")
        return False

    if resp.status_code != 200:
        raise RuntimeError(f"Error fetching: {resp.status_code}")

    # print("⬇ Update found — downloading new file.")
    with open(local_data_path, "wb") as f:
        f.write(resp.content)

    etag = resp.headers.get("ETag")
    last_modified = resp.headers.get("Last-Modified")
    save_local_metadata(local_meta_path, etag, last_modified)

    return True

