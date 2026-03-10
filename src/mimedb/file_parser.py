from magika import Magika
def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    m = Magika()
    res = m.identify_path(args.file)
    print(res.output.label)



if __name__ == "__main__":
    main()

