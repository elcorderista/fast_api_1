from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

#Load env viariables in os.environ
load_dotenv()
class Settings(BaseSettings):
    database_name: str = os.getenv('DATABASE_NAME')
    base_dir: str = os.path.join(os.path.dirname(__file__), '../db')
    databaseURL: str = f'sqlite:///{os.path.join(base_dir, database_name)}'

    app_name: str = os.getenv('APP_NAME')

    jwt_secret_key: str = os.getenv('JWT_SECRET_KEY')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM')

    app_port: int = os.getenv('APP_PORT')
    app_host: str = os.getenv('APP_HOST')
    class Config:
        env_file = '.env'