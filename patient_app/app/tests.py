import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# Set up SQLite database for testing || Configurar banco de dados SQLite para testes
DATABASE_URL = "sqlite:///./patient.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db function to use the sqlite database || Sobrescrever a função get_db para usar o banco de dados sqlite
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables in the test database || Criar tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def sample_patient():
    return {
        "birthdate": "1980-05-10",
        "first": "Fulano",
        "last": "Ciclano",
        "gender": "masculino",
        "address": "Rua Teste, 123",
        "city": "João Pessoa",
        "state": "PB",
        "zip": "58038420"
    }

# Test creating a new patient || Testar a criação de um novo paciente
def test_create_patient(sample_patient):
    response = client.post("/patients/", json=sample_patient)
    assert response.status_code == 200
    data = response.json()
    assert data["first"] == sample_patient["first"]
    assert data["last"] == sample_patient["last"]
    assert "id" in data

# Test retrieving a patient by ID || Testar a recuperação de um paciente por ID
def test_get_patient(sample_patient):
    create_response = client.post("/patients/", json=sample_patient)
    patient_id = create_response.json()["id"]
    
    get_response = client.get(f"/patients/{patient_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == patient_id
    assert data["first"] == sample_patient["first"]

# Test updating a patient || Testar a atualização de um paciente
def test_update_patient(sample_patient):
    create_response = client.post("/patients/", json=sample_patient)
    patient_id = create_response.json()["id"]
    
    updated_data = sample_patient.copy()
    updated_data["last"] = "Beltrano"
    
    update_response = client.put(f"/patients/{patient_id}", json=updated_data)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == patient_id
    assert data["last"] == "Beltrano"

# Test deleting a patient || Testar a exclusão de um paciente
def test_delete_patient(sample_patient):
    create_response = client.post("/patients/", json=sample_patient)
    patient_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/patients/{patient_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == "Patient record deleted successfully"

    # Ensure the patient no longer exists || Garantir que o paciente não existe mais
    get_response = client.get(f"/patients/{patient_id}")
    assert get_response.status_code == 404

# Test searching for a patient || Testar a busca por um paciente
def test_search_patient(sample_patient):
    client.post("/patients/", json=sample_patient)
    
    search_response = client.get("/patients/search/", params={"first": "Fulano"})
    assert search_response.status_code == 200
    data = search_response.json()
    assert len(data) > 0
    assert data[0]["first"] == "Fulano"

    # Search with non-existing name || Buscar com nome inexistente
    search_response = client.get("/patients/search/", params={"first": "NonExisting"})
    assert search_response.status_code == 200
    data = search_response.json()
    assert len(data) == 0