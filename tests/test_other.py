import datetime as dt

import pytest

from streamstats.analysis import Analyser
from streamstats.errors import *
from streamstats.models import AnalysisResult, Event
from streamstats.parsers import CSVParser, JSONLParser
from streamstats.report import Report

"""
Negative tests
"""

def test_wrong_event_error_1():
    with pytest.raises(WrongEventError):
        parser = CSVParser("tests/files/other_a.csv")
        analyser = Analyser(parser)
        analyser.analyse()

def test_wrong_event_error_2():
    with pytest.raises(WrongEventError):
        parser = CSVParser("tests/files/other_b.csv")
        analyser = Analyser(parser)
        analyser.analyse()

def test_file_syntax_error_jsonl():
    with pytest.raises(FileSyntaxError):
        parser = JSONLParser("tests/files/other_c.json")
        analyser = Analyser(parser)
        analyser.analyse()

def test_file_syntax_error_csv():
    with pytest.raises(FileSyntaxError):
        parser = CSVParser("tests/files/other_d.csv")
        analyser = Analyser(parser)
        analyser.analyse()

"""
Positive tests
"""

def test_csv_with_header():
    parser = CSVParser("tests/files/other_e_with_header.csv", has_header=True)
    analyser = Analyser(parser)
    report = Report([analyser.analyse()], 0)
    result = Report()
    result.amount_of_files = 1
    result.amount_of_events = 10
    result.amount_of_skipped = 0
    result.events_by_level_counter = {
        "DEBUG": 3,
        "INFO": 1,
        "WARNING": 0,
        "ERROR": 2,
        "CRITICAL": 4
    }
    result.events_by_source_counter = {
        "something": 4,
        "other": 3,
        "abc": 1,
        "xyz": 1,
        "qqq": 1
    }
    result.top_harmful_sources = ["something", "xyz", "other", "abc"]
    result.first_timestamp = dt.datetime.fromisoformat("2026-07-03").replace(tzinfo=dt.UTC)
    result.last_timestamp = dt.datetime.fromisoformat("2026-07-31").replace(tzinfo=dt.UTC)
    assert report == result

def test_csv_without_header():
    parser = CSVParser("tests/files/other_e_without_header.csv")
    analyser = Analyser(parser)
    report = Report([analyser.analyse()], 0)
    result = Report()
    result.amount_of_files = 1
    result.amount_of_events = 10
    result.amount_of_skipped = 0
    result.events_by_level_counter = {
        "DEBUG": 3,
        "INFO": 1,
        "WARNING": 0,
        "ERROR": 2,
        "CRITICAL": 4
    }
    result.events_by_source_counter = {
        "something": 4,
        "other": 3,
        "abc": 1,
        "xyz": 1,
        "qqq": 1
    }
    result.top_harmful_sources = ["something", "xyz", "other", "abc"]
    result.first_timestamp = dt.datetime.fromisoformat("2026-07-03").replace(tzinfo=dt.UTC)
    result.last_timestamp = dt.datetime.fromisoformat("2026-07-31").replace(tzinfo=dt.UTC)
    assert report == result

def test_utc():
    parser = JSONLParser("tests/files/other_e.json")
    analyser = Analyser(parser)
    report = Report([analyser.analyse()], 0)
    result = Report()
    result.amount_of_files = 1
    result.amount_of_events = 10
    result.amount_of_skipped = 0
    result.events_by_level_counter = {
        "DEBUG": 3,
        "INFO": 1,
        "WARNING": 0,
        "ERROR": 2,
        "CRITICAL": 4
    }
    result.events_by_source_counter = {
        "something": 4,
        "other": 3,
        "abc": 1,
        "xyz": 1,
        "qqq": 1
    }
    result.top_harmful_sources = ["something", "xyz", "other", "abc"]
    # 07-02 23:59 UTC -1 is after 00:00 UTC 07-03
    result.first_timestamp = dt.datetime.fromisoformat("2026-07-03").replace(tzinfo=dt.UTC)
    result.last_timestamp = dt.datetime.fromisoformat("2026-07-31").replace(tzinfo=dt.UTC)
    assert report == result

def test_parser_jsonl():
    result: list = []
    expected: list = [
        Event(dt.datetime.fromisoformat("2026-11-15").replace(tzinfo=dt.UTC), "DEBUG", "cc", "message"),
        Event(dt.datetime.fromisoformat("2026-05-11").replace(tzinfo=dt.UTC), "INFO", "a", "message"),
        Event(dt.datetime.fromisoformat("2026-06-11").replace(tzinfo=dt.UTC), "INFO", "b", "message"),
        Event(dt.datetime.fromisoformat("2026-07-12").replace(tzinfo=dt.UTC), "DEBUG", "a", "message"),
        Event(dt.datetime.fromisoformat("2026-07-17").replace(tzinfo=dt.UTC), "ERROR", "B", "message"),
        Event(dt.datetime.fromisoformat("2026-07-11").replace(tzinfo=dt.UTC), "WARNING", "cc", "message"),
        Event(dt.datetime.fromisoformat("2026-07-17").replace(tzinfo=dt.UTC), "CRITICAL", "кириллица", "message"),
        Event(dt.datetime.fromisoformat("2026-06-30").replace(tzinfo=dt.UTC), "INFO", "22233", "message")
    ]
    parser = JSONLParser("tests/files/other_f.json").parse_file()
    event = next(parser, None)
    while event is not None:
        result.append(event)
        event = next(parser, None)
    assert result == expected

def test_parser_csv():
    result: list = []
    expected: list = [
        Event(dt.datetime.fromisoformat("2026-11-15").replace(tzinfo=dt.UTC), "DEBUG", "cc", "message"),
        Event(dt.datetime.fromisoformat("2026-05-11").replace(tzinfo=dt.UTC), "INFO", "a", "message"),
        Event(dt.datetime.fromisoformat("2026-06-11").replace(tzinfo=dt.UTC), "INFO", "b", "message"),
        Event(dt.datetime.fromisoformat("2026-07-12").replace(tzinfo=dt.UTC), "DEBUG", "a", "message"),
        Event(dt.datetime.fromisoformat("2026-07-17").replace(tzinfo=dt.UTC), "ERROR", "B", "message"),
        Event(dt.datetime.fromisoformat("2026-07-11").replace(tzinfo=dt.UTC), "WARNING", "cc", "message"),
        Event(dt.datetime.fromisoformat("2026-07-17").replace(tzinfo=dt.UTC), "CRITICAL", "кириллица", "message"),
        Event(dt.datetime.fromisoformat("2026-06-30").replace(tzinfo=dt.UTC), "INFO", "22233", "message")
    ]
    parser = CSVParser("tests/files/other_f.csv").parse_file()
    event = next(parser, None)
    while event is not None:
        result.append(event)
        event = next(parser, None)
    assert result == expected

def test_analysis():
    parser = JSONLParser("tests/files/other_f.json")
    analyser = Analyser(parser)
    result = analyser.analyse()
    expected = AnalysisResult(
        8,
        {"DEBUG": 2, "INFO": 3, "WARNING": 1, "CRITICAL": 1, "ERROR": 1},
        {"cc": 2, "a": 2, "b": 1, "B": 1, "кириллица": 1, "22233": 1},
        {"cc": 0, "a": 0, "b": 0, "22233": 0, "B": 1, "кириллица": 1},
        dt.datetime.fromisoformat("2026-05-11").replace(tzinfo=dt.UTC),
        dt.datetime.fromisoformat("2026-11-15").replace(tzinfo=dt.UTC)
    )
    assert result == expected

def test_some_encoding():
    parser = JSONLParser("tests/files/other_e_cp1251.json", encoding="cp1251")
    analyser = Analyser(parser)
    report = Report([analyser.analyse()], 0)
    result = Report()
    result.amount_of_files = 1
    result.amount_of_events = 10
    result.amount_of_skipped = 0
    result.events_by_level_counter = {
        "DEBUG": 3,
        "INFO": 1,
        "WARNING": 0,
        "ERROR": 2,
        "CRITICAL": 4
    }
    result.events_by_source_counter = {
        "что-то": 4,
        "другой": 3,
        "абв": 1,
        "эюя": 1,
        "ыыы": 1
    }
    result.top_harmful_sources = ["что-то", "эюя", "другой", "абв"]
    result.first_timestamp = dt.datetime.fromisoformat("2026-07-03").replace(tzinfo=dt.UTC)
    result.last_timestamp = dt.datetime.fromisoformat("2026-07-31").replace(tzinfo=dt.UTC)
    assert report == result