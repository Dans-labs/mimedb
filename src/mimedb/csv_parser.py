import csv
import json
from pathlib import Path
import schema_types as types

def read_csv_rows(path, sample_size=None, encoding="utf-8"):
    """
    Read CSV rows into dictionaries.

    sample_size limits number of rows used for schema inference.
    """

    rows = []

    with open(path, newline="", encoding=encoding) as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            rows.append(row)

            if sample_size and i + 1 >= sample_size:
                break

    return rows

def infer_csv_schema(path, sample_size=1000):
    """
    Infer schema from a CSV file.
    """

    rows = read_csv_rows(path, sample_size=sample_size)

    if not rows:
        raise ValueError("CSV file contains no rows")

    schema = types.infer_schema(rows)

    schema["source"] = str(Path(path).name)
    schema["rows_sampled"] = len(rows)

    return schema

def schema_fingerprint(schema):
    """
    Compute deterministic schema hash.
    """

    import hashlib

    canonical = types.canonical_schema(schema)

    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()

def csv_mimetype(schema_hash):
    """
    Produce schema-aware CSV mimetype.
    """

    return f"text/csv; schema={schema_hash}"

def main():

    import argparse

    parser = argparse.ArgumentParser(
        description="Infer schema from CSV file"
    )

    parser.add_argument("csv_file")
    parser.add_argument("--sample", type=int, default=1000)

    args = parser.parse_args()

    schema = infer_csv_schema(args.csv_file, args.sample)

    schema_hash = schema_fingerprint(schema)

    mimetype = csv_mimetype(schema_hash)

    print("Schema:")
    print(json.dumps(schema, indent=2))

    print("\nSchema ID:")
    print(schema_hash)

    print("\nMIME type:")
    print(mimetype)


if __name__ == "__main__":
    main()
