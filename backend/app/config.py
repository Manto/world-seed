from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./worldbuilding.db"
    ANTHROPIC_API_KEY: str
    TOGETHER_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
