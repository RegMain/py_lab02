import datetime as dt

TYPES_OF_FIELD: tuple[str] = ("timestamp", "level", "source", "message")
TYPES_OF_LEVEL: tuple[str] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

class Event:
    """
    Type of event, which consists of every field
    that is in TYPES_OF_FIELD. It can be changed
    if needed
    """
    timestamp: dt.datetime
    level: str
    source: str
    message: str

    def __init__(self, timestamp: dt.datetime | None = None,
            level: str = "NONE",
            source: str = "Unknown",
            message: str = ""):
        if timestamp is None:
            self.timestamp = dt.datetime.min.replace(tzinfo=dt.UTC)
        else:
            self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message

    def __eq__(self, event):
        if self.timestamp != event.timestamp:
            return False
        if self.level != event.level:
            return False
        if self.source != event.source:
            return False
        if self.message != event.message:
            return False
        return True

class AnalysisResult:
    """
    Type of result of analysis, which consists of neccessary
    to report facts about file
    """
    amount_of_events: int
    events_by_level_counter: dict
    events_by_source_counter: dict
    harmful_events_by_source_counter: dict
    first_timestamp: dt.datetime
    last_timestamp: dt.datetime

    def __init__(self, amount_of_events: int = 0,
                 events_by_level_counter: dict | None = None,
                 events_by_source_counter: dict | None = None,
                 harmful_events_by_source_counter: dict | None = None,
                 first_timestamp: dt.datetime | None = None,
                 last_timestamp: dt.datetime | None = None):
        self.amount_of_events = amount_of_events
        if events_by_level_counter is None:
            self.events_by_level_counter = {}
        else:
            self.events_by_level_counter = events_by_level_counter
        if events_by_source_counter is None:
            self.events_by_source_counter = {}
        else:
            self.events_by_source_counter = events_by_source_counter
        if harmful_events_by_source_counter is None:
            self.harmful_events_by_source_counter = {}
        else:
            self.harmful_events_by_source_counter = harmful_events_by_source_counter
        if first_timestamp is None:
            self.first_timestamp = dt.datetime.min.replace(tzinfo=dt.UTC)
        else:
            self.first_timestamp = first_timestamp
        if last_timestamp is None:
            self.last_timestamp = dt.datetime.max.replace(tzinfo=dt.UTC)
        else:
            self.last_timestamp = last_timestamp

    def __eq__(self, result):
        if self.amount_of_events != result.amount_of_events:
            return False
        if self.events_by_level_counter != result.events_by_level_counter:
            return False
        if self.events_by_source_counter != result.events_by_source_counter:
            return False
        if self.harmful_events_by_source_counter != result.harmful_events_by_source_counter:
            return False
        if self.first_timestamp != result.first_timestamp:
            return False
        if self.last_timestamp != result.last_timestamp:
            return False
        return True

    def add(self, result):
        """
        Adds given result to this result
        :param result: some AnalysisResult object
        """
        self.amount_of_events += result.amount_of_events
        self.first_timestamp = min(self.first_timestamp, result.first_timestamp)
        self.last_timestamp = max(self.last_timestamp, result.last_timestamp)
        for level, result_value in result.events_by_level_counter.items():
            self.events_by_level_counter[level] += result_value
        for source, result_value in result.events_by_source_counter.items():
            # Uniting the dictionaries
            if source in self.events_by_source_counter:
                self.events_by_source_counter[source] += result_value
                self.harmful_events_by_source_counter[source] += result.harmful_events_by_source_counter[source]
            else:
                self.events_by_source_counter[source] = result_value
                self.harmful_events_by_source_counter[source] = result.harmful_events_by_source_counter[source]

