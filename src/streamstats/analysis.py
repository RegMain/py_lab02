from streamstats.models import (
    Event,
    AnalysisResult
)

from streamstats.parsers import (
    CSVParser,
    JSONLParser
)

from streamstats.errors import(
    IncorrectTimestampError,
    UnknownLevelError
)

import datetime as dt

class Analyser:

    parser: CSVParser | JSONLParser
    skip_invalid: bool
    TYPES_OF_LEVEL: tuple[str] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    def __init__(self, parser: CSVParser | JSONLParser, skip_invalid: bool):
        self.parser = parser.parse_file()
        self.skip_invalid = skip_invalid

    def process_error(self, error: type, line_number: int):
        error_message: str
        if error == IncorrectTimestampError:
            error_message = "Timestamp is wrong"
        elif error == UnknownLevelError:
            error_message = "Event level is unknown"
        else:
            error_message = "Unknown error"
        if self.skip_invalid:
            pass
        else:
            raise error(
                f"{error_message} at line {line_number}.\n"
            )

    def analyse(self) -> dict:
        level_counter: dict = dict()
        source_counter: dict = dict()
        source_harmful_counter: dict = dict()
        first_timestamp = dt.datetime.max
        last_timestamp = dt.datetime.min
        for level in self.TYPES_OF_LEVEL:
            level_counter[level] = 0
        event = next(self.parser, None)
        line_counter = 0
        while event is not None:
            line_counter += 1
            first_timestamp_t: dt.datetime
            last_timestamp_t: dt.datetime
            try:
                event_timestamp = dt.datetime.fromisoformat(event["timestamp"])
                first_timestamp_t = min(first_timestamp, event_timestamp)
                last_timestamp_t = max(last_timestamp, event_timestamp)
            except ValueError:
                self.process_error(self, IncorrectTimestampError, line_counter)
                event = next(self.parser, None)
                continue
            if event["level"] not in self.TYPES_OF_LEVEL:
                self.process_error(UnknownLevelError, line_counter)
                event = next(self.parser, None)
                continue
            else:
                level_counter[event["level"]] += 1
            if event["source"] in source_counter:
                source_counter[event["source"]] += 1
            else:
                source_counter[event["source"]] = 1
                source_harmful_counter[event["source"]] = 0
            source_harmful_counter[event["source"]] += event["level"] in ("ERROR, CRITICAL")
            first_timestamp = first_timestamp_t
            last_timestamp = last_timestamp_t
            event = next(self.parser, None)
        result: AnalysisResult = AnalysisResult(
            line_counter,
            level_counter,
            source_counter,
            source_harmful_counter,
            first_timestamp,
            last_timestamp
        )
        return result

