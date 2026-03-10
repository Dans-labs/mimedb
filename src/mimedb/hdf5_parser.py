import json
import hashlib
import numpy as np
import h5py

def dtype_to_type(dtype):

    if dtype.kind in ("i", "u"):
        return "integer"

    if dtype.kind == "f":
        return "float"

    if dtype.kind == "b":
        return "boolean"

    if dtype.kind in ("S", "O", "U"):
        return "string"

    return "unknown"

def normalize_value(v):

    if isinstance(v, np.generic):
        return v.item()

    if isinstance(v, np.ndarray):
        return v.tolist()

    return v

def dataset_schema(dataset):

    field = {
        "type": "dataset",
        "dtype": dtype_to_type(dataset.dtype),
        "shape": list(dataset.shape)
    }

    if dataset.attrs:
        field["attributes"] = {k: normalize_value(v) for k, v in dataset.attrs.items()}

    return field

def group_schema(group):

    schema = {
        "type": "group",
        "children": {}
    }

    if group.attrs:
        schema["attributes"] = dict(group.attrs)

    for name, item in group.items():

        if isinstance(item, h5py.Dataset):
            schema["children"][name] = dataset_schema(item)

        elif isinstance(item, h5py.Group):
            schema["children"][name] = group_schema(item)

    return schema

def infer_hdf5_schema(path):

    with h5py.File(path, "r") as f:

        schema = {
            "type": "hdf5",
            "root": group_schema(f)
        }

    return schema

def canonical_schema(schema):

    return json.dumps(schema, sort_keys=True, separators=(",", ":"))

def schema_fingerprint(schema):

    canonical = canonical_schema(schema)

    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()

def hdf5_mimetype(schema_hash):

    return f"application/x-hdf5; schema={schema_hash}"

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    schema = infer_hdf5_schema(args.file)

    schema_id = schema_fingerprint(schema)

    mimetype = hdf5_mimetype(schema_id)

    print("Schema:")
    print(json.dumps(schema, indent=2))

    print("\nSchema ID:")
    print(schema_id)

    print("\nMIME type:")
    print(mimetype)


if __name__ == "__main__":
    main()
