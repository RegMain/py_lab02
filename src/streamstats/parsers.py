import datetime as dt

from streamstats.errors import (
    IncorrectTimeStampError,
    FileSyntaxError
)
class StreamStatsParser():
    file_name: str
    skip_invalid: bool
    encoding: str

    def __init__(self, file_name: str, skip_invalid: bool = False, encoding: str = "UTF-8"):
        self.file_name = file_name
        self.skip_invalid = skip_invalid
        self.encoding = encoding

    def process_error(self, error: Exception, line_number: int):
        if self.skip_invalid:
            pass
        else:
            error_message: str
            match error:
                case FileSyntaxError:
                    error_message = "Syntax is wrong"
                case IncorrectTimeStampError:
                    error_message = "Timestamp is wrong"
                case _:
                    error_message = "Unknown error"

            raise error(
                f"{error_message} at line {line_number}.\n"
            )

    def is_earlier(self, first_datetime: str, second_datetime: str) -> bool:
        try:
            return dt.datetime.fromisoformat(first_datetime) < dt.datetime.fromisoformat(second_datetime)
        except ValueError:
            return False

class JSONLParser(StreamStatsParser):

    TYPES_OF_FIELD: tuple[str] = ("\"timestamp\"", "\"level\"", "\"source\"", "message\"")
    LEVELS_OF_EVENT: tuple[str] = ("\"DEBUG\"", "\"INFO\"", "\"WARNING\"", "\"ERROR\"", "\"CRITICAL\"")

    def field_is_correct(self, string: str, is_type: bool, type: str = "", line_number: int) -> bool:
        if not string or string[0] != "\"" or string[-1] != "\"":
            return False
        if is_type:
            return string in self.TYPES_OF_FIELD
        else:
            match type:
                case "timestamp":
                    try:
                        tmp = dt.datetime.fromisoformat(string[1:-1])
                    except ValueError:
                        self.process_error(IncorrectTimeStampError, line_number)
                        return False
                case "level":
                    return string in self.LEVELS_OF_EVENT
                case "source":
                    return len(string) > 2
                case "message":
                    return True
                case _:
                    return False

    def parse_line(self, line: str, line_number: int):
        if not line:
            return
        if line[0] != "{" or line[-2] != "}":
            raise FileSyntaxError(
                f"JSONL syntax in file is wrong at line {line_number}.\n"
            )
        fields: list[str] = line[1:-2].split(",")
        for field in fields:
            field_type, field_value = map(lambda x: x.strip(), field.split(":"))
            if not self.field_is_correct(field_type, True, line_number=line_number):
                raise FileSyntaxError(
                    f"JSONL syntax in file is wrong at line {line_number}.\n"
                )
            field_type = field_type[1:-1]
            if not self.field_is_correct(field_value, False, type=field_type, line_number=line_number):
                raise FileSyntaxError(
                    f"JSONL syntax in file is wrong at line {line_number}.\n"
                )
            field_value = field_value[1:-1]



    def parse_file(self):
        with open(self.file_name, mode="r", encoding=self.encoding) as file:
            line: str
            line_counter: int = 0
            while (line := file.readline()) != "":
                line_counter += 1
                self.parse_line(line, line_counter)