import mimedb as mdb

def main():
    db = mdb.types2extensions()
    print("Available types and their extensions:")
    for key in db.keys():
        print(f"{key}: {db[key]}")

    print("\n-----------------------\n")

    db2 = mdb.extensions2types()
    print("\nAvailable extensions and their types:")
    for key in db2.keys():
        print(f"{key}: {db2[key]}")


if __name__ == "__main__":
    main()
