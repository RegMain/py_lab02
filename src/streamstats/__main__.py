from streamstats.parsers import JSONLParser, CSVParser
from streamstats.analysis import Analyser
from streamstats.report import Report
from streamstats.errors import StreamStatsError

def main():
    try:
        parser = JSONLParser("a.txt", False)
        analyser = Analyser(parser, False)
        report = Report([analyser.analyse()])
        report.write()
    except StreamStatsError as error:
        print(error)

if __name__ == "__main__":
    main()