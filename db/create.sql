-- This is for SQLite3

CREATE TABLE buoy_reading (
    reading_id INTEGER PRIMARY KEY,
    create_time CHAR(80),
    buoy_id CHAR(20)
);

CREATE TABLE wave_data (
    wave_data_id INTEGER PRIMARY KEY,
    reading_id INTEGER,
    wave_height REAL,
    wave_mean_period REAL,
    wave_peak_period REAL,
    wave_dir CHAR,
    swell_ht REAL,
    swell_period REAL,
    swell_dir CHAR,
    wind_ht REAL,
    wind_period REAL,
    wind_dir CHAR
);

CREATE TABLE general_data (
    general_data_id INTEGER PRIMARY KEY,
    reading_id INTEGER,
    atmo_pressure REAL,
    water_temp REAL,
    air_temp REAL
);

CREATE TABLE wind_data (
    wind_data_id INTEGER PRIMARY KEY,
    wind_speed REAL,
    wind_dir CHAR(10),
    reading_id INTEGER
);

CREATE TABLE buoy_info (
    id PRIMARY KEY,
    name CHAR(10) NOT NULL,
    coord CHAR(40),
    active INTEGER
);
