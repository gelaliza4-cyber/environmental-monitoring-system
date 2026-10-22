
import csv
import os
from datetime import datetime, timezone
from pathlib import Path

import psycopg


# Locate the CSV file
csv_path = Path(__file__).resolve().parent.parent / "data" / os.getenv(
    "CSV_FILE", "sample_sensor_data.csv"
)

# Database connection settings
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "environmental_db"),
    "user": os.getenv("DB_USER", "envuser"),
    "password": os.environ["DB_PASSWORD"],
}

BATCH_SIZE = 1000

INSERT_SQL = """
INSERT INTO measurements
    (ts, device, co, humidity, light, lpg, motion, smoke, temp)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (device, ts) DO NOTHING
"""


def convert_boolean(value):
    value = value.strip().lower()

    if value == "true":
        return True
    if value == "false":
        return False

    raise ValueError(f"Invalid boolean: {value}")


def prepare_record(row):
    timestamp = datetime.fromtimestamp(
        float(row["ts"]),
        tz=timezone.utc
    )

    return (
        timestamp,
        row["device"],
        float(row["co"]),
        float(row["humidity"]),
        convert_boolean(row["light"]),
        float(row["lpg"]),
        convert_boolean(row["motion"]),
        float(row["smoke"]),
        float(row["temp"]),
    )


def main():
    processed = 0
    inserted = 0
    rejected = 0
    batch = []
    csv_path = Path(__file__).resolve().parent.parent / "data" / os.getenv(
    "CSV_FILE", "sample_sensor_data.csv"
)

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            with open(csv_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row_number, row in enumerate(reader, start=2):
                    try:
                        record = prepare_record(row)
                        batch.append(record)
                        processed += 1

                    except (ValueError, KeyError, TypeError, OverflowError) as error:
                        rejected += 1
                        print(f"Invalid row {row_number}: {error}")
                        continue

                    if len(batch) >= BATCH_SIZE:
                        cur.executemany(INSERT_SQL, batch)
                        inserted += cur.rowcount
                        conn.commit()
                        batch.clear()

                if batch:
                    cur.executemany(INSERT_SQL, batch)
                    inserted += cur.rowcount
                    conn.commit()

    print("Import completed.")
    print(f"Valid records processed: {processed}")
    print(f"Records inserted: {inserted}")
    print(f"Invalid records skipped: {rejected}")


if __name__ == "__main__":
    main()




