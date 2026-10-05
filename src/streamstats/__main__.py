from streamstats.parsers import JSONLParser

def main():
    parser = JSONLParser("a.txt", False)
    print(parser.parse_file())

if __name__ == "__main__":
    main()