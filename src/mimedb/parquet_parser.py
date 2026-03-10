import json
import hashlib
import pyarrow.parquet as pq
import pyarrow.types as pat

def arrow_type_to_type(t):

    if pat.is_integer(t):
        return "integer"

    if pat.is_floating(t):
        return "float"

    if pat.is_boolean(t):
        return "boolean"

    if pat.is_string(t):
        return "string"

    if pat.is_binary(t):
        return "binary"

    if pat.is_timestamp(t):
        return "datetime"

    if pat.is_list(t):
        return "array"

    if pat.is_struct(t):
        return "object"

    return "unknown"

def field_schema(field):

    t = field.type

    base = {
        "name": field.name,
        "type": arrow_type_to_type(t)
    }

    if pat.is_struct(t):

        base["properties"] = {
            f.name: field_schema(f)
            for f in t
        }

    elif pat.is_list(t):

        base["items"] = field_schema(t.value_field)

    return base

def infer_parquet_schema(path):

    parquet_file = pq.ParquetFile(path)

    schema = parquet_file.schema_arrow

    fields = []

    for field in schema:
        fields.append(field_schema(field))

    return {
        "type": "parquet",
        "fields": fields
    }

def canonical_schema(schema):

    return json.dumps(schema, sort_keys=True, separators=(",", ":"))

def schema_fingerprint(schema):

    canonical = canonical_schema(schema)

    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()

def parquet_mimetype(schema_hash):

    return f"application/x-parquet; schema={schema_hash}"

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    schema = infer_parquet_schema(args.file)

    schema_id = schema_fingerprint(schema)

    mimetype = parquet_mimetype(schema_id)

    print("Schema:")
    print(json.dumps(schema, indent=2))

    print("\nSchema ID:")
    print(schema_id)

    print("\nMIME type:")
    print(mimetype)


if __name__ == "__main__":
    main()

