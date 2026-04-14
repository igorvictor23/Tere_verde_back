from pydantic_settings import BaseSettings

# cria uma classe para acessar o .env e utilizar a váriaveis
class Settings(BaseSettings):

    DATABASE_URL : str
    SECRET_JWT : str
    ALGORITHM : str
    GEMINI_API_KEY : str

    class Config:
        env_file = "../.env"
        case_sensitive = True



settings = Settings()