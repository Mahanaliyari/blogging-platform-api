from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent


# This pydantic class verifies the env variables from .env
# We will call the variables from this class later in our program 
class Settings(BaseSettings):
     
    secret_key: str
    sqlalchemy_database_url: str
    algorithm: str 
    access_token_expire_minutes: int 
    
    # This will actually call the env variables from ".env" file
    # We have to define the specific path to ".env" file  
    model_config = SettingsConfigDict(
        env_file= Path(__file__).resolve().parent / ".env"
    )

        

setting = Settings() # type: ignore