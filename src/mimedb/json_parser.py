"""
Infer a schema from a JSON file.

Works for:
- JSON arrays of objects
- single JSON objects
- nested JSON structures
"""

import json
from collections import Counter

import schema_types as types


# ------------------------------
# JSON reader
# ------------------------------

def load_json(path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------
# recursive type detection
# ------------------------------

def infer_value_schema(value):

    if value is None:
        return {"type": "null"}

    if isinstance(value, bool):
        return {"type": "boolean"}

    if isinstance(value, int):
        return {"type": "integer"}

    if isinstance(value, float):
        return {"type": "float"}

    if isinstance(value, str):

        t = types.detect_value_type(value)

        if t == "json":
            try:
                obj = json.loads(value)
                return infer_value_schema(obj)
            except Exception:
                return {"type": "string"}

        if t == "geometry":
            geom = types.detect_wkt_type(value)
            return types.geometry_schema(geom)

        return {"type": t}

    if isinstance(value, list):

        if not value:
            return {"type": "array"}

        item_schemas = [infer_value_schema(v) for v in value]

        return {
            "type": "array",
            "items": merge_schemas(item_schemas)
        }

    if isinstance(value, dict):

        props = {}

        for k, v in value.items():
            props[k] = infer_value_schema(v)

        return {
            "type": "object",
            "properties": props
        }

    return {"type": "string"}


# ------------------------------
# schema merging
# ------------------------------

def merge_schemas(schemas):

    if not schemas:
        return {"type": "unknown"}

    types_seen = [s.get("type") for s in schemas]

    most_common = Counter(types_seen).most_common(1)[0][0]

    if most_common == "object":

        merged = {}

        for s in schemas:
            props = s.get("properties", {})
            for k, v in props.items():
                merged.setdefault(k, []).append(v)

        properties = {}

        for k, vals in merged.items():
            properties[k] = merge_schemas(vals)

        return {
            "type": "object",
            "properties": properties
        }

    if most_common == "array":

        items = [s.get("items") for s in schemas if "items" in s]

        return {
            "type": "array",
            "items": merge_schemas(items)
        }

    return {"type": most_common}


# ------------------------------
# top-level inference
# ------------------------------

def infer_json_schema(path):

    data = load_json(path)

    if isinstance(data, list):

        schemas = [infer_value_schema(v) for v in data]

        schema = merge_schemas(schemas)

    else:
        schema = infer_value_schema(data)

    return schema


# ------------------------------
# canonical schema
# ------------------------------

def canonical_schema(schema):

    return json.dumps(schema, sort_keys=True, separators=(",", ":"))


# ------------------------------
# schema fingerprint
# ------------------------------

def schema_fingerprint(schema):

    import hashlib

    canonical = canonical_schema(schema)

    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


# ------------------------------
# CLI
# ------------------------------

def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("json_file")

    args = parser.parse_args()

    schema = infer_json_schema(args.json_file)

    schema_id = schema_fingerprint(schema)

    print("Schema:")
    print(json.dumps(schema, indent=2))

    print("\nSchema ID:")
    print(schema_id)


if __name__ == "__main__":
    main()

