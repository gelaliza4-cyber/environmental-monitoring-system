
import csv
from collections import Counter
from pathlib import Path

csv_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "iot_telemetry_data.csv"
)

combinations = Counter()

with open(csv_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        key = (row["device"], float(row["ts"]))
        combinations[key] += 1

total_records = sum(combinations.values())
unique_combinations = len(combinations)
duplicates = total_records - unique_combinations

print(f"Total CSV records: {total_records}")
print(f"Unique device/timestamp combinations: {unique_combinations}")
print(f"Duplicate combinations: {duplicates}")
