import mimedb as mdb

def main():
    types= ["text/plain", "application/json", "image/jpeg", "galaxy.datatypes.text:Json"]
    for t in types:
        equivalents = mdb.equivalent_types(t)
        print(f"Equivalent types for '{t}': {equivalents}")

if __name__ == "__main__":
    main()
