from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'PowerOfData Star Wars API'
    VERSION: str = '1.0.0'
    DESCRIPTION: str = 'API para explorar o universo Star Wars com filtros avançados'
    QUESTIONS_FILE: str = 'app/assets/questions.py'
    SWAPI_BASE_URL: str
    APIKEY_MARICATA: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
