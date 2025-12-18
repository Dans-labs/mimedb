import mimedb as mdb

def main():
    types= ["text/plain", "application/json", "image/jpeg", "galaxy.datatypes.text:Json"]
    for t in types:
        equivalents = mdb.equivalent_types(t)
        print(f"Equivalent types for '{t}': {equivalents}")
        extensions = mdb.get_extensions(t)
        print(f"Extensions for '{t}': {extensions}")
        for ext in extensions:
            types_for_ext = mdb.get_types(ext)
            print(f"Types for extension '{ext}': {types_for_ext}")

        print("-" * 40)

if __name__ == "__main__":
    main()
