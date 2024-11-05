from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from database import get_db

router = APIRouter()

# Create a new patient record || Criar uma nova entry na tabela de pacientes
@router.post("/patients/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientBase, db: Session = Depends(get_db)):
    db_patient = models.Patient(
        birthdate=patient.birthdate,
        deathdate=patient.deathdate,
        ssn=patient.ssn,
        drivers=patient.drivers,
        passport=patient.passport,
        prefix=patient.prefix,
        first=patient.first,
        middle=patient.middle,
        last=patient.last,
        suffix=patient.suffix,
        maiden=patient.maiden,
        marital=patient.marital,
        race=patient.race,
        ethnicity=patient.ethnicity,
        gender=patient.gender,
        birthplace=patient.birthplace,
        address=patient.address,
        city=patient.city,
        state=patient.state,
        county=patient.county,
        fips=patient.fips,
        zip=patient.zip,
        lat=patient.lat,
        lon=patient.lon,
        healthcare_expenses=patient.healthcare_expenses,
        healthcare_coverage=patient.healthcare_coverage,
        income=patient.income,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Retrieve a patient record by ID || Receber uma entry de paciente por ID
@router.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

# Update a patient record by ID || Atualizar uma entry de paciente por ID
@router.put("/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: int, patient_update: schemas.PatientBase, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    for field, value in patient_update.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Delete a patient record by ID || Deletar uma entry de paciente por ID
@router.delete("/patients/{patient_id}", response_model=dict)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return {"message": "Patient record deleted successfully"}

# Search for patients based on specific fields || Procurar por pacientes baseado em campos específicos
@router.get("/patients/search/", response_model=List[schemas.PatientResponse])
def search_patients(
    first: Optional[str] = Query(None),
    last: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Patient)

    # Add filters based on provided query parameters || Adicionar filtros baseado nos parâmetros de query fornecidos
    if first:
        query = query.filter(models.Patient.first.ilike(f"%{first}%"))
    if last:
        query = query.filter(models.Patient.last.ilike(f"%{last}%"))
    if gender:
        query = query.filter(models.Patient.gender.ilike(f"%{gender}%"))
    if city:
        query = query.filter(models.Patient.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(models.Patient.state.ilike(f"%{state}%"))

    results = query.all()
    return results
