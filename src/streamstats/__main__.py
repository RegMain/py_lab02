from streamstats.parsers import JSONLParser, CSVParser
from streamstats.analysis import Analyser
from streamstats.report import Report

def main():
    parser = CSVParser("a.csv", False)
    analyser = Analyser(parser, False)
    report = Report([analyser.analyse()])
    report.write()

if __name__ == "__main__":
    main()