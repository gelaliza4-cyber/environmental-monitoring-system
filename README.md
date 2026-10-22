# Environmental Monitoring System

## Project Overview

This project uses Python and PostgreSQL to process and store environmental sensor data. The goal is to simulate a monitoring system for apartment buildings, where unusual measurements could be identified and investigated.

## Dataset

**Source:** [Environmental Sensor Telemetry Data – Kaggle](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k)

The dataset contains 405,184 measurements from three devices, including temperature, humidity, and air quality indicators. After excluding 13 duplicates, 405,171 measurements were stored in PostgreSQL.

## Tools Used

- **Python:** Processes and imports the data in batches.
- **PostgreSQL:** Stores the measurements.
- **Docker Compose:** Runs the database and Python importer in containers.

## How to Run

1. Install Docker Desktop and make sure it is running.
2. Open PowerShell in the project folder.
3. Run the following commands:

```powershell
$env:DB_PASSWORD = "your-local-password"
docker compose up --build -d
```

To check the import results:

```powershell
docker compose logs importer
```

To check the number of measurements stored:

```powershell
docker compose exec database psql -U envuser -d environmental_db -c "SELECT COUNT(*) FROM measurements;"
```

The project automatically imports 100 simulated sensor measurements into PostgreSQL.

## Future Development

The database could later include buildings, apartments, and rooms. The stored data could also be used to identify measurements that exceed defined thresholds.