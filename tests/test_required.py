from streamstats.analysis import Analyser
from streamstats.parsers import JSONLParser, CSVParser
from streamstats.report import Report
import datetime as dt

"""
Required tests
"""

def test_empty_report():
    parser_jsonl = JSONLParser("tests/files/empty_file.txt")
    analyser_jsonl = Analyser(parser_jsonl)
    report_jsonl = Report([analyser_jsonl.analyse()], parser_jsonl.warnings_counter)

    assert report_jsonl.is_empty()

    parser_csv = CSVParser("tests/files/empty_file.txt")
    analyser_csv = Analyser(parser_csv)
    report_csv = Report([analyser_csv.analyse()], parser_csv.warnings_counter)

    assert report_csv.is_empty()

def test_equal_files():
    parser_jsonl = JSONLParser("tests/files/required_a.json")
    analyser_jsonl = Analyser(parser_jsonl)
    report_jsonl = Report([analyser_jsonl.analyse()], parser_jsonl.warnings_counter)

    parser_csv = CSVParser("tests/files/required_a.csv")
    analyser_csv = Analyser(parser_csv)
    report_csv = Report([analyser_csv.analyse()], parser_csv.warnings_counter)

    assert report_jsonl == report_csv

def test_multiple_files():
    parser_1 = JSONLParser("tests/files/required_a.json")
    parser_2 = JSONLParser("tests/files/required_b.json")
    analyser_1 = Analyser(parser_1)
    analyser_2 = Analyser(parser_2)
    report = Report(
        [analyser_1.analyse(), analyser_2.analyse()],
        parser_1.warnings_counter + parser_2.warnings_counter
    )

    result = Report
    result.amount_of_files = 2
    result.amount_of_events = 15
    result.amount_of_skipped = 0
    result.events_by_source_counter = {
        "Unknown": 1,
        "Aybolit": 7,
        "Euler": 1,
        "Someone": 1,
        "IUseArchBTW": 1,
        "中國": 2,
        "Euclid": 1,
        "Yay": 1
    }
    result.events_by_level_counter = {
        "DEBUG": 1,
        "INFO": 4,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 5
    }
    result.top_harmful_sources = ["Aybolit", "中國", "Someone", "Euclid"]
    result.first_timestamp = dt.datetime.fromisoformat("2025-01-10").replace(tzinfo=dt.UTC)
    result.last_timestamp = dt.datetime.fromisoformat("2025-02-27").replace(tzinfo=dt.UTC)

    assert report == result

def test_cyrillic():
    parser = JSONLParser("tests/files/required_c.json")
    analyser = Analyser(parser)
    report = Report([analyser.analyse()], parser.warnings_counter)

    assert sorted(["Кто я", "Не знаю", "Мда"]) == sorted(list(report.events_by_source_counter.keys()))

def test_line_7():
    with open("tests/warnings_d.log", "w"):
        pass
    parser = JSONLParser("tests/files/required_d.json", skip_invalid=True, warnings_file="tests/warnings_d.log")
    analyser = Analyser(parser)
    analyser.analyse()
    with open("tests/warnings_d.log", "r") as warnings_file:
        warnings = warnings_file.read()
        assert "at line 7." in warnings

def test_incorrect_timestamp():
    with open("tests/warnings_d.log", "w"):
        pass
    parser = JSONLParser("tests/files/required_d.json", skip_invalid=True, warnings_file="tests/warnings_d.log")
    analyser = Analyser(parser)
    analyser.analyse()
    with open("tests/warnings_d.log", "r") as warnings_file:
        warnings = warnings_file.read()
        assert "Timestamp" in warnings and "at line 4." in warnings
