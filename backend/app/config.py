from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./worldbuilding.db"
    ANTHROPIC_API_KEY: str = ""
    TOGETHER_API_KEY: str = ""

    class Config:
        env_file = ".env"
        # Try multiple possible locations for .env file
        env_file_paths = [
            Path(".env"),  # Current directory
            Path("../.env"),  # Parent directory
            Path(__file__).parent.parent / ".env",  # Project root
        ]


settings = Settings()

# For debugging
if __name__ == "__main__":
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Anthropic API Key: {'set' if settings.ANTHROPIC_API_KEY else 'not set'}")
    print(f"Looking for .env in: {Settings.Config.env_file_paths}")
