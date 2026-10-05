import datetime as dt

class Event:
    timestamp: dt.datetime
    level: str
    source: str
    message: str

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

