import tomllib
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, FilePath, SecretStr, Field, computed_field


class Settings(BaseSettings):
    environment: str
    log_level: str = Field(default="INFO")


class ChainSettings(BaseSettings):
    params_path: FilePath = Field(default="/data/params/rag.toml")
    openai_api_key: SecretStr

    @computed_field
    def chain_params(self) -> dict:
        with open(self.params_path, "rb") as file:
            return tomllib.load(file)


class MemorySettings(BaseSettings):
    memory_connection: PostgresDsn
    collection_name: str


class VectordbSettings(BaseSettings):
    vectordb_connection: PostgresDsn
    collection_name: str
    knowledge_base_path: FilePath = Field(default="./data/knowledge_base.csv")
    embedding_cols: str
    rebuild_db: bool = Field(default=True)


settings = Settings()
chain_settings = ChainSettings(_env_file=".env", _env_file_encoding="utf-8")
memory_settings = MemorySettings(_env_file=".env", _env_file_encoding="utf-8")
vectordb_settings = VectordbSettings(_env_file=".env", _env_file_encoding="utf-8")
