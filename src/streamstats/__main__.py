import argparse
import sys

from streamstats.parsers import (
    StreamStatsParser,
    JSONLParser,
    CSVParser
)
from streamstats.analysis import Analyser
from streamstats.report import Report
from streamstats.errors import (
    StreamStatsError,
    UnsupportedFormatError
)
from streamstats.models import AnalysisResult

def main():
    argument_parser = argparse.ArgumentParser(
        prog="streamstats", description="StreamStats: CLI Analyser of logs"
    )
    argument_subparsers = argument_parser.add_subparsers(dest="command", required=True)
    main_parser = argument_subparsers.add_parser(
        "analyze",
        help="Syntax: analyze INPUT [INPUT ...] --format csv|jsonl"
    )
    main_parser.add_argument("input", nargs="+")
    main_parser.add_argument("--format", type=str, required=True)
    main_parser.add_argument("--output", type=str, default="")
    main_parser.add_argument("--encoding", type=str, default="UTF-8")
    main_parser.add_argument("--skip-invalid", action="store_true")

    args = main_parser.parse_args()
    try:
        result: list[AnalysisResult] = []
        for file_name in args.input:
            file_parser: StreamStatsParser
            if args.skip_invalid:
                # Clearing the warning log
                tmp_file = open("warnings.log", "w")
                tmp_file.close()
            match args.format:
                case "csv":
                    file_parser = CSVParser(file_name, args.skip_invalid, args.encoding)
                case "jsonl":
                    file_parser = JSONLParser(file_name, args.skip_invalid, args.encoding)
                case _:
                    raise UnsupportedFormatError(
                        f"Format \"{args.format}\" is unsupported.\n"
                    )
            file_analyser = Analyser(file_parser)
            result.append(file_analyser.analyse())
        report = Report(result, file_parser.warnings_counter)
        report.write()
        if args.output:
            report.write_json(args.output)
    except StreamStatsError as error:
        sys.stderr.write(f"Error: {error}")
        sys.exit(2)

if __name__ == "__main__":
    main()