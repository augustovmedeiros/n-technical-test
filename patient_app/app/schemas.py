from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

# Define the schema for the Patient model || Definir o estrutura para o modelo de Paciente
class PatientBase(BaseModel):
    birthdate: date
    deathdate: Optional[date] = None
    ssn: Optional[str] = None
    drivers: Optional[str] = None
    passport: Optional[str] = None
    prefix: Optional[str] = None
    first: str
    middle: Optional[str] = None
    last: str
    suffix: Optional[str] = None
    maiden: Optional[str] = None
    marital: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    gender: Optional[str] = None
    birthplace: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    county: Optional[str] = None
    fips: Optional[str] = None
    zip: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    healthcare_expenses: Optional[float] = None
    healthcare_coverage: Optional[float] = None
    income: Optional[int] = None

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility with SQLAlchemy models || Habilitar compatibilidade ORM com modelos SQLAlchemy
