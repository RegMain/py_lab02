import csv
import datetime as dt
import json

from streamstats.models import TYPES_OF_LEVEL, AnalysisResult


class Report:
    """
    Class for report of work, writes pretty-looking result
    in CLI and (optionally) csv and/or jsonl file
    """

    amount_of_files: int
    amount_of_events: int
    amount_of_skipped: int
    events_by_level_counter: dict
    events_by_source_counter: dict
    top_harmful_sources: list
    first_timestamp: dt.datetime | None
    last_timestamp: dt.datetime | None

    def __init__(self, results: list[AnalysisResult] | None = None, warnings_counter: int = 0):
        if results is None:
            results = [AnalysisResult()]
        self.amount_of_files = len(results)
        overall_result: AnalysisResult = results[0]
        # We sum up results of every file
        for result in results[1:]:
            overall_result.add(result)
        self.amount_of_events = overall_result.amount_of_events
        self.amount_of_skipped = warnings_counter
        self.events_by_level_counter = overall_result.events_by_level_counter
        self.events_by_source_counter = overall_result.events_by_source_counter
        harmful_sources: list[tuple] = list(overall_result.harmful_events_by_source_counter.items())
        harmful_sources.sort(key=lambda x: (x[1], x[0]), reverse=True)
        self.top_harmful_sources = []
        # Organizing the top X, where x in 0..5 (you can easily change it)
        for i in range(1, min(len(harmful_sources) + 1, 6)):
            if harmful_sources[i - 1][1] > 0:
                self.top_harmful_sources.append(harmful_sources[i - 1][0])
            else:
                break
        # If it's true then files are blank or totally wrong
        if overall_result.last_timestamp == dt.datetime.min.replace(tzinfo=dt.UTC):
            self.first_timestamp = None
            self.last_timestamp = None
        else:
            self.first_timestamp = overall_result.first_timestamp
            self.last_timestamp = overall_result.last_timestamp

    def __eq__(self, result):
        is_equal: bool = True
        is_equal = is_equal and self.amount_of_files == result.amount_of_files
        is_equal = is_equal and self.amount_of_events == result.amount_of_events
        is_equal = is_equal and self.amount_of_skipped == result.amount_of_skipped
        is_equal = is_equal and self.events_by_level_counter == result.events_by_level_counter
        is_equal = is_equal and self.events_by_source_counter == result.events_by_source_counter
        is_equal = is_equal and self.top_harmful_sources == result.top_harmful_sources
        is_equal = is_equal and self.first_timestamp == result.first_timestamp
        is_equal = is_equal and self.last_timestamp == result.last_timestamp
        return is_equal

    def is_empty(self):
        """
        Decides, if this Report is empty (no events were provided) or not.
        :return: result of computing
        """
        is_empty: bool = True
        is_empty = is_empty and self.amount_of_events == 0
        is_empty = is_empty and self.events_by_level_counter == dict(zip(TYPES_OF_LEVEL, [0 for _ in range(len(TYPES_OF_LEVEL))]))
        is_empty = is_empty and self.events_by_source_counter == {}
        is_empty = is_empty and self.top_harmful_sources == []
        is_empty = is_empty and self.first_timestamp is None
        is_empty = is_empty and self.last_timestamp is None
        return is_empty

    def write_csv(self, file_name: str):
        """
        Writes report in CSV format
        :param file_name: output file name
        """
        with open(file_name, "w") as report_file:
            csv_report = csv.writer(report_file, delimiter=",")
            csv_report.writerow(["parameter", "value"])
            csv_report.writerow(["amount of files", self.amount_of_files])
            csv_report.writerow(["amount of events", self.amount_of_events])
            csv_report.writerow(["amount of skipped", self.amount_of_skipped])
            csv_report.writerow(["events by level",
                *(": ".join([str(i) for i in x] for x in self.events_by_level_counter.items()))])
            csv_report.writerow(["events by source",
                *(": ".join([str(i) for i in x] for x in self.events_by_source_counter.items()))])
            csv_report.writerow(["top harmful sources", *self.top_harmful_sources])
            csv_report.writerow(["first timestamp", self.first_timestamp.isoformat()])
            csv_report.writerow(["last timestamp", self.last_timestamp.isoformat()])

    def write_json(self, file_name: str):
        """
        Writes report in JSON Lines format
        :param file_name: output file name
        """
        json_report = {}
        json_report["amounts_of_files"] = self.amount_of_files
        json_report["amount_of_events"] = self.amount_of_events
        json_report["amount_of_skipped"] = self.amount_of_skipped
        json_report["events_by_level"] = self.events_by_level_counter
        json_report["events_by_source"] = self.events_by_source_counter
        json_report["top_harmful_sources"] = self.top_harmful_sources
        if self.last_timestamp is None:
            json_report["first_timestamp"] = None
            json_report["last_timestamp"] = None
        else:
            json_report["first_timestamp"] = self.first_timestamp.isoformat()
            json_report["last_timestamp"] = self.last_timestamp.isoformat()
        with open(file_name, "w") as report_file:
            json.dump(json_report, report_file, indent=4)

    def write(self):
        """
        Runs by default. Writes report in CLI
        """
        print("================STREAMSTATS================")
        print(f"-- Result for {self.amount_of_files} file(s)")
        print(f"Amount of events: {self.amount_of_events}")
        if self.is_empty():
            return
        if self.amount_of_skipped > 0:
            print(f"WARNING: {self.amount_of_skipped} event(s) was skipped. See ./warnings.log\n")
        else:
            print()
        print("AMOUNT OF EVENTS BY LEVEL")
        for level in TYPES_OF_LEVEL:
            print(f"{level}: {self.events_by_level_counter[level]}")
        print()
        print("AMOUNT OF EVENTS BY SOURCE")
        for source, value in self.events_by_source_counter.items():
            print(f"\"{source}\": {value}")
        print()
        print(f"TOP {len(self.top_harmful_sources)} HARMFUL EVENT SOURCES")
        for i in range(1, len(self.top_harmful_sources) + 1):
            print(f"{i}. \"{self.top_harmful_sources[i - 1]}\"")
        print()
        if self.last_timestamp is None:
            print("First timestamp: None\nLast timestamp: None")
        else:
            print(f"First timestamp: {self.first_timestamp.isoformat()}")
            print(f"Last timestamp: {self.last_timestamp.isoformat()}")
        print("-- End of report")
