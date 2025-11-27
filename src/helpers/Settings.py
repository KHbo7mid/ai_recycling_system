from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    IMAGE_SIZE:int
    
    class Config:
        case_sensitive=True
        env_file = ".env"
        
        
get_settings=Settings()