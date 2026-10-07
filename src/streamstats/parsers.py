import json
import csv
import datetime as dt

from streamstats.errors import (
    FileSyntaxError,
    IncorrectTimestampError,
    WrongEventError
)
from streamstats.models import TYPES_OF_FIELD, TYPES_OF_LEVEL, Event

class StreamStatsParser():

    file_name: str
    skip_invalid: bool
    encoding: str
    warnings_counter: int = 0

    def __init__(self, file_name: str, skip_invalid: bool = False, encoding: str = "UTF-8"):
        self.file_name = file_name
        self.skip_invalid = skip_invalid
        self.encoding = encoding

    def process_error(self, error: type, line_number: int):
        error_message: str
        if error == FileSyntaxError:
            error_message = "File syntax is wrong"
        elif error == WrongEventError:
            error_message = "Event is wrong"
        elif error == IncorrectTimestampError:
            error_message = "Timestamp is incorrect"
        else:
            error_message = "Unknown error"
        if not self.skip_invalid:
            raise error(
                f"{error_message} at line {line_number}.\n"
            )
        else:
            with open("warnings.log", "a") as warnings_file:
                if self.warnings_counter == 0:
                    warnings_file.write(f"\n-- File \"{self.file_name}\"\n")
                warnings_file.write(f"WARNING: {error_message} at line {line_number}.\n")
                self.warnings_counter += 1

    def check_event(self, event: Event, line_number: int) -> bool:
        if event.level not in TYPES_OF_LEVEL:
            self.process_error(WrongEventError, line_number)
            return False
        if not event.source:
            self.process_error(WrongEventError, line_number)
            return False
        return True

class JSONLParser(StreamStatsParser):

    def parse_line(self, line: str, line_number: int) -> dict:
        if not line.strip():
            return dict()
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            self.process_error(FileSyntaxError, line_number)
            return dict()

    def parse_file(self) -> dict:
        with open(self.file_name, mode="r", encoding=self.encoding) as file:
            line: str
            line_counter: int = 0
            while (line := file.readline()) != "":
                line_counter += 1
                data: dict = self.parse_line(line, line_counter)
                if len(data) == 0:
                    continue
                if tuple(data.keys()) != TYPES_OF_FIELD:
                    self.process_error(FileSyntaxError, line_counter)
                    continue
                try:
                    data["timestamp"] = dt.datetime.fromisoformat(data["timestamp"])
                except ValueError:
                    self.process_error(IncorrectTimestampError, line_counter)
                    continue
                event: Event = Event(*data.values())
                if not self.check_event(event, line_counter):
                    continue
                yield event

class CSVParser(StreamStatsParser):

    def parse_file(self) -> dict:
        with open(self.file_name, mode="r", encoding=self.encoding) as file:
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(sample=file.read(1024))
            file.seek(0)
            reader = csv.DictReader(file, fieldnames=None if has_header else TYPES_OF_FIELD, delimiter=",")
            line_counter: int = 0
            for line in reader:
                line_counter += 1
                if len(line) != len(TYPES_OF_FIELD):
                    self.process_error(FileSyntaxError, line_counter)
                    continue
                try:
                    line["timestamp"] = dt.datetime.fromisoformat(line["timestamp"])
                except ValueError:
                    self.process_error(IncorrectTimestampError, line_counter)
                    continue
                event: Event = Event(*line.values())
                if not self.check_event(event, line_counter):
                    continue
                yield event