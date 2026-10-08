import datetime as dt

TYPES_OF_FIELD: tuple[str] = ("timestamp", "level", "source", "message")
TYPES_OF_LEVEL: tuple[str] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

class Event:
    timestamp: dt.datetime
    level: str
    source: str
    message: str

    def __init__(self, timestamp: dt.datetime, level: str, source: str, message: str):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message

class AnalysisResult:
    amount_of_events: int
    events_by_level_counter: dict
    events_by_source_counter: dict
    harmful_events_by_source_counter: dict
    first_timestamp: dt.datetime
    last_timestamp: dt.datetime

    def __init__(self, amount_of_events: int,
                 events_by_level_counter: dict,
                 events_by_source_counter: dict,
                 harmful_events_by_source_counter: dict,
                 first_timestamp: dt.datetime,
                 last_timestamp: dt.datetime):
        self.amount_of_events = amount_of_events
        self.events_by_level_counter = events_by_level_counter
        self.events_by_source_counter = events_by_source_counter
        self.harmful_events_by_source_counter = harmful_events_by_source_counter
        self.first_timestamp = first_timestamp
        self.last_timestamp = last_timestamp

    def add(self, result):
        self.amount_of_events += result.amount_of_events
        self.first_timestamp = min(self.first_timestamp, result.first_timestamp)
        self.last_timestamp = max(self.last_timestamp, result.last_timestamp)
        for level, result_value in result.events_by_level_counter.items():
            self.events_by_level_counter[level] += result_value
        for source, result_value in result.events_by_source_counter.items():
            if source in self.events_by_source_counter:
                self.events_by_source_counter[source] += result_value
                self.harmful_events_by_source_counter[source] += result.harmful_events_by_source_counter[source]
            else:
                self.events_by_source_counter[source] = result_value
                self.harmful_events_by_source_counter[source] = result.harmful_events_by_source_counter[source]

