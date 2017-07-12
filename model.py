from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class GeneralData(Base):
    __tablename__ = 'general_data'

    reading_id = Column(String, ForeignKey("buoy_reading.reading_id"), primary_key=True)
    water_temp = Column(String(50), unique=True)
    air_temp = Column(String(120), unique=True)
    atmo_pressure = Column(String(120), unique=True)

    def __init__(self, reading_id=None, water_temp=None, air_temp=None, atmo_pressure=None):
        self.reading_id = reading_id
        self.water_temp = water_temp
        self.air_temp = air_temp
        self.atmo_pressure = atmo_pressure

    def __repr__(self):
        return '<GeneralData %r>' % (self.reading_id)


class WaveData(Base):
  __tablename__ = 'wave_data'

  reading_id = Column(String, ForeignKey("buoy_reading.reading_id"), primary_key=True)
  wave_height = Column(String(50))
  wave_mean_period = Column(String(120))
  wave_peak_period = Column(String)
  wave_dir = Column(String(50))
  swell_ht = Column(String(120))
  swell_period = Column(String)
  swell_dir = Column(String(50))
  wind_ht = Column(String(120))
  wind_period = Column(String)
  wind_dir = Column(String(50))

  def __init__(self, reading_id=None, wave_height=None, wave_mean_period=None, wave_peak_period=None,
               wave_dir=None, swell_ht=None, swell_period=None, swell_dir=None, wind_ht=None, wind_period=None,
               wind_dir=None):
    self.reading_id = reading_id
    self.wave_height = wave_height
    self.wave_mean_period = wave_mean_period
    self.wave_peak_period = wave_peak_period
    self.wave_dir = wave_dir
    self.swell_ht = swell_ht
    self.swell_period = swell_period
    self.swell_dir = swell_dir
    self.wind_ht = wind_ht
    self.wind_period = wind_period
    self.wind_dir = wind_dir

  def __repr__(self):
    return '<WaveData %r>' % (self.name)


class BuoyReading(Base):
  __tablename__ = 'buoy_reading'

  reading_id = Column(String, primary_key=True)
  buoy_id = Column(String(60))
  create_time = Column(String(120))

  wave_data = relationship("WaveData")
  general_data = relationship("GeneralData")

  def __init__(self, reading_id=None, buoy_id=None, create_time=None):
    self.reading_id = reading_id
    self.buoy_id = buoy_id
    self.create_time = create_time

  def __repr__(self):
    return '<BuoyReading %r>' % (self.reading_id)
