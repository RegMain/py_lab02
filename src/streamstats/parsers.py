import json
import csv

from streamstats.errors import FileSyntaxError

class StreamStatsParser():

    file_name: str
    skip_invalid: bool
    encoding: str

    def __init__(self, file_name: str, skip_invalid: bool = False, encoding: str = "UTF-8"):
        self.file_name = file_name
        self.skip_invalid = skip_invalid
        self.encoding = encoding

    def process_error(self, error: type, line_number: int):
        if self.skip_invalid:
            pass
        else:
            error_message: str
            if error == FileSyntaxError:
                error_message = "Syntax is wrong"
            else:
                error_message = "Unknown error"
            raise error(
                f"{error_message} at line {line_number}.\n"
            )

class JSONLParser(StreamStatsParser):

    def parse_line(self, line: str, line_number: int) -> dict:
        if not line:
            return dict()
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            self.process_error(FileSyntaxError, line_number)
            return dict()

    def parse_file(self) -> list[dict]:
        with open(self.file_name, mode="r", encoding=self.encoding) as file:
            line: str
            line_counter: int = 0
            result: list = list()
            while (line := file.readline()) != "":
                line_counter += 1
                result.append(self.parse_line(line, line_counter))
            return result



class CSVParser(StreamStatsParser):

    def parse_file(self) -> list[dict]:
        with open(self.file_name, mode="r", encoding=self.encoding) as file:
            reader = csv.reader(file, delimiter=";", quotechar="\"")
            line_counter: int = 0
            result: list = list()
            for line in reader:
                line_counter += 1
                result.append(line)


