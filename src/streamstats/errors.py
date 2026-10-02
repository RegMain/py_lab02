class StreamStatsError(Exception):
    pass

class UnsupportedFormatError(StreamStatsError):
    pass

class InvalidEventError(StreamStatsError):
    pass

class IncorrectTimeStampError(StreamStatsError):
    pass

class FileSyntaxError(StreamStatsError):
    pass

class ConfigurationError(StreamStatsError):
    pass