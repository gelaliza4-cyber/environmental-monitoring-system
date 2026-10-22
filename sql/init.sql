
CREATE TABLE IF NOT EXISTS measurements (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    device VARCHAR(100) NOT NULL,
    co DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    light BOOLEAN,
    lpg DOUBLE PRECISION,
    motion BOOLEAN,
    smoke DOUBLE PRECISION,
    temp DOUBLE PRECISION,

    CONSTRAINT unique_device_timestamp UNIQUE (device, ts),
    CONSTRAINT valid_humidity CHECK (
        humidity IS NULL OR
        (humidity >= 0 AND humidity <= 100)
    )
);

CREATE INDEX IF NOT EXISTS idx_measurements_device_ts
ON measurements (device, ts);
