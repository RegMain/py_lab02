from streamstats.models import (
    AnalysisResult,
    TYPES_OF_LEVEL
)

import json

class Report:

    results: list[AnalysisResult]
    warnings_counter: int

    def __init__(self, results: list[AnalysisResult], warnings_counter: int):
        self.results = results
        self.warnings_counter = warnings_counter

    def write(self):
        overall_result: AnalysisResult = self.results[0]
        json_report = dict()
        for result in self.results[1:]:
            overall_result.add(result)
        print("================STREAMSTATS================")
        print(f"-- Result for {len(self.results)} file(s)")
        print(f"Amount of events: {overall_result.amount_of_events}")
        if self.warnings_counter > 0:
            print(f"WARNING: {self.warnings_counter} event(s) was skipped. See ./warnings.log\n")
        else:
            print()
        json_report["amount_of_events"] = overall_result.amount_of_events
        print(f"AMOUNT OF EVENTS BY LEVEL")
        for level in TYPES_OF_LEVEL:
            print(f"{level}: {overall_result.events_by_level_counter[level]}")
        json_report["events_by_level"] = overall_result.events_by_level_counter
        print()
        print("AMOUNT OF EVENTS BY SOURCE")
        for source, value in overall_result.events_by_source_counter.items():
            print(f"\"{source}\": {value}")
        json_report["events_by_source"] = overall_result.events_by_source_counter
        print()
        print("TOP 5 HARMFUL EVENT SOURCES")
        harmful_sources: list[tuple] = list(overall_result.harmful_events_by_source_counter.items())
        harmful_sources.sort(key=lambda x: x[1], reverse=True)
        json_report["top5_harmful_sources"] = []
        for i in range(1, min(len(harmful_sources) + 1, 6)):
            print(f"{i}. \"{harmful_sources[i - 1][0]}\"")
            json_report["top5_harmful_sources"].append(harmful_sources[i - 1][0])
        print()
        print(f"First timestamp: {overall_result.first_timestamp.isoformat()}")
        json_report["first_timestamp"] = overall_result.first_timestamp.isoformat()
        print(f"Last timestamp: {overall_result.last_timestamp.isoformat()}")
        json_report["last_timestamp"] = overall_result.last_timestamp.isoformat()
        print(f"-- End of report")
        with open("report.json", "w") as report_file:
            json.dump(json_report, report_file, indent=4)
