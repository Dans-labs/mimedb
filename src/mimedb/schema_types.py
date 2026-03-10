import re
import json
import uuid
import ipaddress
from datetime import datetime
from collections import Counter


# ------------------------------
# regex patterns
# ------------------------------

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
URL_RE = re.compile(r"^https?://")
INT_RE = re.compile(r"^-?\d+$")
FLOAT_RE = re.compile(r"^-?\d+\.\d+$")
BOOL_VALUES = {"true", "false", "yes", "no", "0", "1"}

# WKT geometry keywords
WKT_PREFIXES = (
    "POINT",
    "LINESTRING",
    "POLYGON",
    "MULTIPOINT",
    "MULTILINESTRING",
    "MULTIPOLYGON",
    "GEOMETRYCOLLECTION",
)


# ------------------------------
# primitive detectors
# ------------------------------

def is_null(v: str):
    if v is None:
        return True
    s = str(v).strip().lower()
    return s in {"", "null", "na", "n/a", "none"}


def is_int(v: str):
    return bool(INT_RE.match(v))


def is_float(v: str):
    return bool(FLOAT_RE.match(v))


def is_bool(v: str):
    return str(v).lower() in BOOL_VALUES


def is_uuid(v: str):
    try:
        uuid.UUID(v)
        return True
    except Exception:
        return False


def is_ip(v: str):
    try:
        ipaddress.ip_address(v)
        return True
    except Exception:
        return False


def is_email(v: str):
    return bool(EMAIL_RE.match(v))


def is_url(v: str):
    return bool(URL_RE.match(v))


def is_datetime(v: str):
    try:
        datetime.fromisoformat(v)
        return True
    except Exception:
        return False


def is_json(v: str):
    try:
        obj = json.loads(v)
        return isinstance(obj, (dict, list))
    except Exception:
        return False


def is_wkt(v: str):
    if not isinstance(v, str):
        return False
    s = v.strip().upper()
    return any(s.startswith(p) for p in WKT_PREFIXES)


# ------------------------------
# value type detection
# ------------------------------

def detect_value_type(v: str):
    """
    Detect type of a single value.
    """

    if is_null(v):
        return "null"

    if is_bool(v):
        return "boolean"

    if is_int(v):
        return "integer"

    if is_float(v):
        return "float"

    if is_uuid(v):
        return "uuid"

    if is_ip(v):
        return "ip"

    if is_email(v):
        return "email"

    if is_url(v):
        return "url"

    if is_datetime(v):
        return "datetime"

    if is_json(v):
        return "json"

    if is_wkt(v):
        return "geometry"

    return "string"


# ------------------------------
# column inference
# ------------------------------

def detect_column_type(values):
    """
    Infer a column type from sample values.
    """

    types = []

    for v in values:
        t = detect_value_type(v)
        if t != "null":
            types.append(t)

    if not types:
        return "null"

    counts = Counter(types)

    # choose most common type
    return counts.most_common(1)[0][0]


# ------------------------------
# enum detection
# ------------------------------

def detect_enum(values, threshold=20):
    unique = set(v for v in values if not is_null(v))

    if 0 < len(unique) <= threshold:
        return sorted(unique)

    return None


# ------------------------------
# numeric statistics
# ------------------------------

def numeric_stats(values):

    nums = []

    for v in values:
        try:
            nums.append(float(v))
        except Exception:
            pass

    if not nums:
        return None

    return {
        "minimum": min(nums),
        "maximum": max(nums),
    }

def infer_json_schema(values):
    """
    Infer schema of JSON objects stored in a column.
    """

    objects = []

    for v in values:
        if is_null(v):
            continue

        try:
            obj = json.loads(v)
            if isinstance(obj, dict):
                objects.append(obj)
        except Exception:
            continue

    if not objects:
        return {"type": "object"}

    keys = {}

    for obj in objects:
        for k, v in obj.items():
            keys.setdefault(k, []).append(v)

    properties = {}

    for k, vals in keys.items():

        vals = [str(v) for v in vals if v is not None]

        t = detect_column_type(vals)

        properties[k] = {"type": t}

    return {
        "type": "object",
        "properties": properties
    }

def detect_wkt_type(v: str):

    if not isinstance(v, str):
        return None

    s = v.strip().upper()

    for t in WKT_PREFIXES:
        if s.startswith(t):
            return t.lower()

    return None

def geometry_schema(geom_type):

    if geom_type == "point":
        return {
            "type": "object",
            "geometry": "Point",
            "properties": {
                "type": {"const": "Point"},
                "coordinates": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2
                }
            }
        }

    if geom_type == "linestring":
        return {
            "type": "object",
            "geometry": "LineString",
            "properties": {
                "type": {"const": "LineString"},
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2
                    }
                }
            }
        }

    if geom_type == "polygon":
        return {
            "type": "object",
            "geometry": "Polygon",
            "properties": {
                "type": {"const": "Polygon"},
                "coordinates": {
                    "type": "array"
                }
            }
        }

    if geom_type == "multipoint": 
        return { 
            "type": "object", 
            "geometry": "MultiPoint", 
            "properties": { 
                "type": {"const": "MultiPoint"}, 
                "coordinates": { 
                    "type": "array", 
                    "items": { 
                        "type": "array", 
                        "items": { "type": "number" }, 
                        "minItems": 2, 
                        "maxItems": 2 
                    } 
                } 
            }
        } 

    if geom_type == "multilinestring": 
        return { 
            "type": "object", 
            "geometry": "MultiLineString", 
            "properties": { 
                "type": {"const": "MultiLineString"}, 
                "coordinates": { 
                    "type": "array", 
                    "items": { 
                        "type": "array", 
                        "items": { 
                            "type": "array", 
                            "items": {"type": "number"}, 
                            "minItems": 2, 
                            "maxItems": 2 
                        } 
                    } 
                } 
            } 
        } 
    
    if geom_type == "multipolygon": 
        return { 
            "type": "object", 
            "geometry": "MultiPolygon", 
            "properties": { 
                "type": {"const": "MultiPolygon"}, 
                "coordinates": { 
                    "type": "array", 
                    "items": { 
                        "type": "array", 
                        "items": { 
                            "type": "array", 
                            "items": { 
                                "type": "array", 
                                "items": {"type": "number"}, 
                                "minItems": 2, 
                                "maxItems": 2 
                            } 
                        } 
                    } 
                } 
            } 
        } 

    if geom_type == "geometrycollection": 
        return { 
            "type": "object", 
            "geometry": "GeometryCollection", 
            "properties": { 
                "type": {"const": "GeometryCollection"}, 
                "geometries": { 
                    "type": "array", 
                    "items": { "type": "object" } 
                } 
            } 
        }


    return {
        "type": "object",
        "geometry": geom_type
    }

# ------------------------------
# schema generation
# ------------------------------

def infer_schema(rows):
    """
    Infer schema from list of dict rows.
    """

    columns = {}

    for row in rows:
        for k, v in row.items():
            columns.setdefault(k, []).append(v)

    schema = {"fields": []}

    for col, values in columns.items():

        col_type = detect_column_type(values)

        field = {
            "name": col,
            "type": col_type,
        }

        if col_type == "json":
            field["schema"] = infer_json_schema(values)

        if col_type == "geometry":

            geom_types = [
                detect_wkt_type(v)
                for v in values
                if v and detect_wkt_type(v)
            ]

            if geom_types:
                geom_type = Counter(geom_types).most_common(1)[0][0]
                field["schema"] = geometry_schema(geom_type)

        # enum_vals = detect_enum(values)
        # if enum_vals:
        #     field["enum"] = enum_vals

        stats = numeric_stats(values)
        if stats and col_type in ("integer", "float"):
            field.update(stats)

        schema["fields"].append(field)

    schema["fields"] = sorted(schema["fields"], key=lambda f: f["name"])

    return schema


# ------------------------------
# canonical schema
# ------------------------------

def canonical_schema(schema):
    """
    Produce deterministic schema string for hashing.
    """
    return json.dumps(schema, sort_keys=True, separators=(",", ":"))


# ------------------------------
# example
# ------------------------------

# if __name__ == "__main__":
#
#     rows = [
#         {
#             "id": "123",
#             "year": "1990",
#             "email": "a@example.org",
#             "geom": "POINT(1 2)"
#         },
#         {
#             "id": "124",
#             "year": "2000",
#             "email": "b@example.org",
#             "geom": "POINT(3 4)"
#         },
#     ]
#
#     schema = infer_schema(rows)
#
#     print(json.dumps(schema, indent=2))
#
