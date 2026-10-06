class StreamStatsError(Exception):
    pass

class UnsupportedFormatError(StreamStatsError):
    pass

class WrongEventError(StreamStatsError):
    pass

class IncorrectTimestampError(StreamStatsError):
    pass

class FileSyntaxError(StreamStatsError):
    pass

class ConfigurationError(StreamStatsError):
    pass