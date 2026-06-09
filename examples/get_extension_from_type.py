import mimedb as mdb

def main():
    json_ext = mdb.get_extensions("application/json")
    print(f"Extensions for type 'application/json': {json_ext}")
    csv_ext = mdb.get_extensions("text/csv")
    print(f"Extensions for type 'text/csv': {csv_ext}")

if __name__ == "__main__":
    main()
