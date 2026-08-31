from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent


''' Settings defines the application's configuration schema. 
BaseSettings obtains values from supported settings sources—including 
environment variables and the configured .env file and 
Pydantic parses/validates those values against the declared types.
We will call the variables from this class later in our program '''

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



'''.env stores configuration → Settings defines what configuration is expected → 
Settings() loads and validates it → 
setting gives the rest of your application convenient access to it.'''