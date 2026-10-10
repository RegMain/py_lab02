import pytest
from streamstats.errors import *
from streamstats.parsers import CSVParser, JSONLParser
from streamstats.analysis import Analyser

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
    pass

def test_csv_without_header():
    pass

def test_jsonl():
    pass

def test_analysis():
    pass

def test_parser_jsonl():
    pass

def test_parser_csv():
    pass