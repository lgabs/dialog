import tomllib
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, FilePath, SecretStr, Field, computed_field


class Settings(BaseSettings):
    environment: str
    logging_level: str = Field(default="INFO")


class ChainSettings(BaseSettings):
    params_path: FilePath = Field(default="/data/params.toml")
    openai_api_key: SecretStr

    @computed_field
    def chain_params(self) -> dict:
        with open(self.params_path, "rb") as file:
            return tomllib.load(file)


class MemorySettings(BaseSettings):
    connection: PostgresDsn
    collection_name: str


class VectordbSettings(BaseSettings):
    connection: PostgresDsn
    collection_name: str
    knowledge_base_path: FilePath = Field(default="./data/knowledge_base.csv")


settings = Settings()
chain_settings = ChainSettings(_env_file=".env", _env_file_encoding="utf-8")
memory_settings = MemorySettings(_env_file=".env", _env_file_encoding="utf-8")
vectordb_settings = VectordbSettings(_env_file=".env", _env_file_encoding="utf-8")
