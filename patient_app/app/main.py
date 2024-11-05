from fastapi import FastAPI
from routes import router as patient_router
from database import engine
import models

# Create database tables || Criar tabelas do banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes || Definir rotas
app.include_router(patient_router)
