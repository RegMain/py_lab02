import datetime as dt

from streamstats.models import TYPES_OF_LEVEL, AnalysisResult, Event
from streamstats.parsers import StreamStatsParser


class Analyser:

    parser: StreamStatsParser

    def __init__(self, parser: StreamStatsParser):
        self.parser = parser.parse_file()

    def analyse(self) -> AnalysisResult:
        level_counter: dict = {}
        source_counter: dict = {}
        source_harmful_counter: dict = {}
        first_timestamp = dt.datetime.max.replace(tzinfo=dt.UTC)
        last_timestamp = dt.datetime.min.replace(tzinfo=dt.UTC)
        for level in TYPES_OF_LEVEL:
            level_counter[level] = 0
        event: Event = next(self.parser, None)
        line_counter = 0
        while event is not None:
            line_counter += 1
            if not event:
                event = next(self.parser, None)
                continue
            first_timestamp = min(first_timestamp, event.timestamp)
            last_timestamp = max(last_timestamp, event.timestamp)
            level_counter[event.level] += 1
            if event.source in source_counter:
                source_counter[event.source] += 1
            else:
                source_counter[event.source] = 1
                source_harmful_counter[event.source] = 0
            source_harmful_counter[event.source] += int(event.level in ("ERROR, CRITICAL"))
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

