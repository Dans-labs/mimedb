import mimedb as mdb

def main():
    fasta_types = mdb.get_types("fasta")
    print(f"Types for 'fasta' extension: {fasta_types}")
    json_ext = mdb.get_extensions("application/json")
    print(f"Extensions for type 'application/json': {json_ext}")

if __name__ == "__main__":
    main()
