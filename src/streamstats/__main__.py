import argparse
import sys

from streamstats.analysis import Analyser
from streamstats.errors import (
    ConfigurationError,
    StreamStatsError,
    UnsupportedFormatError,
)
from streamstats.models import AnalysisResult
from streamstats.parsers import CSVParser, JSONLParser, StreamStatsParser
from streamstats.report import Report


def main():
    """
    Main point of program. Parses command line arguments
    and analyses every provided file to write report.
    """
    argument_parser = argparse.ArgumentParser(
        prog="streamstats", description="StreamStats: CLI JSONL and CSV statistics utility"
    )
    argument_subparsers = argument_parser.add_subparsers(dest="command", required=True)
    main_parser = argument_subparsers.add_parser(
        "analyze",
        help="Syntax: analyze INPUT [INPUT ...] --format csv|jsonl"
    )
    # CLI Arguments and Flags
    main_parser.add_argument("input", nargs="+", help="Names of files you need to analyse")
    main_parser.add_argument("--format", type=str, required=True, help="Format of your files")
    main_parser.add_argument("--json_report", type=str, default="", help="Name of json report file")
    main_parser.add_argument("--csv_report", type=str, default="", help="Name of csv report file")
    main_parser.add_argument("--encoding", type=str, default="UTF-8", help="Encoding of json file (csv is not supported)")
    main_parser.add_argument("--skip-invalid", action="store_true", help="Errors are writen in warnings.log if it's true, else error ends the program.")
    main_parser.add_argument("--header", action="store_true", help="If it's true then header is present in given csv files")
    args = main_parser.parse_args()

    # Program itself
    try:
        result: list[AnalysisResult] = []
        warnings_counter = 0
        if args.skip_invalid:
            # Clearing the warning log
            with open("warnings.log", "w"):
                pass
        for file_name in args.input:
            # Read every file
            file_parser: StreamStatsParser
            match args.format:
                case "csv":
                    file_parser = CSVParser(file_name, args.skip_invalid, has_header=args.header)
                case "jsonl":
                    file_parser = JSONLParser(file_name, args.skip_invalid, encoding=args.encoding)
                case _:
                    raise UnsupportedFormatError(
                        f"Format \"{args.format}\" is unsupported.\n"
                    )
            file_analyser = Analyser(file_parser)
            try:
                result.append(file_analyser.analyse())
            except FileNotFoundError:
                raise ConfigurationError(
                    f"File \"{file_name}\" is not found.\n"
                )
            except LookupError:
                raise ConfigurationError(
                    f"Encoding \"{args.encoding}\" is unknown.\n"
                )
            warnings_counter += file_parser.warnings_counter
        report = Report(result, warnings_counter)
        report.write()
        if args.json_report:
            report.write_json(args.json_report)
        if args.csv_report:
            report.write_csv(args.csv_report)
    except StreamStatsError as error:
        sys.stderr.write(f"Error: {error}")
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()