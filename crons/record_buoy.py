#!/usr/bin/env python

import syslog
import sqlite3
from buoyant import Buoy

import swell_journal_config

ATTR_WATER_TEMP = 'sea_water_temperature'
ATTR_AIR_TEMP = 'air_temperature'
ATTR_PRESSURE = 'air_pressure_at_sea_level'

ATTR_GROUP_WAVES = 'waves'
ATTR_WAVE_SIG_HEIGHT = 'sea_surface_wave_significant_height'
ATTR_WAVE_PERIOD_MEAN = 'sea_surface_wave_mean_period'
ATTR_WAVE_PERIOD_PEAK = 'sea_surface_wave_peak_period'
ATTR_WAVE_DIRECTION = 'sea_surface_wave_to_direction'
ATTR_SWELL_SIG_HEIGHT = 'sea_surface_swell_wave_significant_height'
ATTR_SWELL_PERIOD = 'sea_surface_swell_wave_period'
ATTR_SWELL_DIRECTION = 'sea_surface_swell_wave_to_direction'
ATTR_WIND_WAVE_SIG_HEIGHT = 'sea_surface_wind_wave_significant_height'
ATTR_WIND_WAVE_PERIOD = 'sea_surface_wind_wave_period'
ATTR_WIND_WAVE_DIRECTION = 'sea_surface_wind_wave_to_direction'

def get_active_buoys():
    with sqlite3.connect(swell_journal_config.DATABASE_URI, timeout=3) as connection:
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(" SELECT *"
                       " FROM buoy_info"
                       " WHERE active=1")
        active_buoys = cursor.fetchall()
    if connection:
        connection.close()
    return active_buoys


def format_general_data(buoy_data):
    return (
        buoy_data.sea_water_temperature if hasattr(buoy_data, ATTR_WATER_TEMP) else None,
        buoy_data.air_temperature if hasattr(buoy_data, ATTR_AIR_TEMP) else None,
        buoy_data.air_pressure_at_sea_level if hasattr(buoy_data, ATTR_PRESSURE) else None
    )


def format_wave_data(buoy_data):
    if hasattr(buoy_data, ATTR_GROUP_WAVES) and buoy_data.waves != None:
        wave_attributes = (ATTR_WAVE_SIG_HEIGHT,
                           ATTR_WAVE_PERIOD_MEAN,
                           ATTR_WAVE_PERIOD_PEAK,
                           ATTR_WAVE_DIRECTION,
                           ATTR_SWELL_SIG_HEIGHT,
                           ATTR_SWELL_PERIOD,
                           ATTR_SWELL_DIRECTION,
                           ATTR_WIND_WAVE_SIG_HEIGHT,
                           ATTR_WIND_WAVE_PERIOD,
                           ATTR_WIND_WAVE_DIRECTION)
        buoy_wave_data = buoy_data.waves

        wave_data = ()
        for wave_attribute in wave_attributes:
            if wave_attribute in buoy_wave_data:
                if buoy_wave_data[wave_attribute] is not None:
                    wave_data = wave_data + (buoy_wave_data[wave_attribute],)
                else:
                    wave_data = wave_data + (None,)
            else:
                wave_data = wave_data + (None,)
        return wave_data

    return (None, None, None, None, None, None, None, None, None, None)


def insert_buoy_reading(cursor, buoy_id):
    cursor.execute("INSERT INTO buoy_reading("
                   "  create_time,"
                   "  buoy_id"
                   ") VALUES ((DATETIME('now')), ?)",
                   (buoy_id,))


def insert_general_data(cursor, general_data):
    cursor.execute("INSERT INTO general_data("
                   "  reading_id,"
                   "  water_temp,"
                   "  air_temp,"
                   "  atmo_pressure"
                   ") VALUES(?, ?, ?, ?)", general_data)


def insert_wave_data(cursor, wave_data):
    cursor.execute("INSERT INTO wave_data("
                   "  reading_id,"
                   "  wave_height,"
                   "  wave_mean_period,"
                   "  wave_peak_period,"
                   "  wave_dir,"
                   "  swell_ht,"
                   "  swell_period,"
                   "  swell_dir,"
                   "  wind_ht,"
                   "  wind_period,"
                   "  wind_dir"
                   ") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", wave_data)

def get_buoy_reading(buoy_id):
    return Buoy(buoy_id)

def insert_buoy_readings():
    active_buoys = get_active_buoys()
    for buoy in active_buoys:
        buoy_id = buoy[0]
        reading = get_buoy_reading(buoy_id)
        with sqlite3.connect(swell_journal_config.DATABASE_URI, timeout=3) as connection:
            try:
                cursor = connection.cursor()
                insert_buoy_reading(cursor, buoy_id)
                reading_id = cursor.lastrowid

                general_data = (reading_id,) + format_general_data(reading)
                insert_general_data(cursor, general_data)

                wave_data = (reading_id,) + format_wave_data(reading)
                insert_wave_data(cursor, wave_data)
            except:
                connection.rollback()
                syslog.syslog('ERROR! Inserting buoy info for ' + str(buoy_id))
            finally:
                syslog.syslog(syslog.LOG_INFO, '[BUOY READING] Added for ' + str(buoy_id))
        if connection:
            connection.close()

if __name__ == '__main__':
    insert_buoy_readings()
