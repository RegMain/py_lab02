import datetime as dt

TYPES_OF_FIELD: tuple[str] = ("timestamp", "level", "source", "message")
TYPES_OF_LEVEL: tuple[str] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

class Event:
    timestamp: dt.datetime
    level: str
    source: str
    message: str

    def __init__(self, timestamp: dt.datetime = dt.datetime.min.replace(tzinfo=dt.UTC),
            level: str = "NONE",
            source: str = "Unknown",
            message: str = ""):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message

    def __eq__(self, event):
        is_equal: bool = True
        is_equal = is_equal and self.timestamp == event.timestamp
        is_equal = is_equal and self.level == event.level
        is_equal = is_equal and self.source == event.source
        is_equal = is_equal and self.message == event.message
        return is_equal

class AnalysisResult:
    amount_of_events: int
    events_by_level_counter: dict
    events_by_source_counter: dict
    harmful_events_by_source_counter: dict
    first_timestamp: dt.datetime
    last_timestamp: dt.datetime

    def __init__(self, amount_of_events: int = 0,
                 events_by_level_counter: dict = {},
                 events_by_source_counter: dict = {},
                 harmful_events_by_source_counter: dict = {},
                 first_timestamp: dt.datetime = dt.datetime.min.replace(tzinfo=dt.UTC),
                 last_timestamp: dt.datetime = dt.datetime.max.replace(tzinfo=dt.UTC)):
        self.amount_of_events = amount_of_events
        self.events_by_level_counter = events_by_level_counter
        self.events_by_source_counter = events_by_source_counter
        self.harmful_events_by_source_counter = harmful_events_by_source_counter
        self.first_timestamp = first_timestamp
        self.last_timestamp = last_timestamp

    def __eq__(self, result):
        is_equal: bool = True
        is_equal = is_equal and self.amount_of_events == result.amount_of_events
        is_equal = is_equal and self.events_by_level_counter == result.events_by_level_counter
        is_equal = is_equal and self.events_by_source_counter == result.events_by_source_counter
        is_equal = is_equal and self.harmful_events_by_source_counter == result.harmful_events_by_source_counter
        is_equal = is_equal and self.first_timestamp == result.first_timestamp
        is_equal = is_equal and self.last_timestamp == result.last_timestamp
        return is_equal

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

