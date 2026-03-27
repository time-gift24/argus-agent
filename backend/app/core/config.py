from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "argus-agents"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./argus_agents.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
