from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "admin"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "patient_db"
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?client_encoding=utf8"

    class Config:
        env_file = ".env"  # Load environment variables from a .env file || Carregar variáveis de ambiente de um arquivo .env 

settings = Settings()
