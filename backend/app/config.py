from typing import Literal, Union
import dotenv
from pydantic_ai.models import KnownModelName
from pydantic_settings import BaseSettings, SettingsConfigDict
import logfire

dotenv.load_dotenv()


def scrubbing_callback(m: logfire.ScrubMatch):
    return m.value


logfire.configure(scrubbing=logfire.ScrubbingOptions(callback=scrubbing_callback))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite:///./worldbuilding.db"
    USE_LOCAL_MODEL: bool = False
    AI_MODEL: KnownModelName | str = ""
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    TOGETHER_API_KEY: str = ""


settings = Settings()

# For debugging
if __name__ == "__main__":
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Anthropic API Key: {'set' if settings.ANTHROPIC_API_KEY else 'not set'}")
    print(f"Looking for .env in: {Settings.Config.env_file_paths}")
