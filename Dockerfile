
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY data/sample_sensor_data.csv ./data/sample_sensor_data.csv

CMD ["python", "scripts/import_data.py"]
