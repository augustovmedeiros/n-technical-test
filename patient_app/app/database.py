from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config import settings

# Create database engine || Criar engine de banco de dados
engine = create_engine(settings.DATABASE_URL)

# Create session factory || Criar criador de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models || Classe base para modelos SQLAlchemy
Base = declarative_base()

# Function to get DB session | Função para pegar sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
