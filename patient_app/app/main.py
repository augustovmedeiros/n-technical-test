from fastapi import FastAPI
from .routes import router
from .database import engine
from .models import Base

# Create database tables || Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes || Definir rotas
app.include_router(router)
