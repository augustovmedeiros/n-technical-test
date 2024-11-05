from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    birthdate = Column(Date, nullable=False)
    deathdate = Column(Date, nullable=True)
    ssn = Column(String, nullable=True)
    drivers = Column(String, nullable=True)
    passport = Column(String, nullable=True)
    prefix = Column(String, nullable=True)
    first = Column(String, nullable=False)
    middle = Column(String, nullable=True)
    last = Column(String, nullable=False)
    suffix = Column(String, nullable=True)
    maiden = Column(String, nullable=True)
    marital = Column(String, nullable=True)
    race = Column(String, nullable=True)
    ethnicity = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birthplace = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    county = Column(String, nullable=True)
    fips = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    healthcare_expenses = Column(Float, nullable=True)
    healthcare_coverage = Column(Float, nullable=True)
    income = Column(Integer, nullable=True)
