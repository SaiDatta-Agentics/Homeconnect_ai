from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "HomeConnect AI"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret-change-in-production"
    access_token_expire_minutes: int = 720
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./homeconnect.db"
    ai_provider: str = "dummy"
    azure_openai_endpoint: str = ""
    azure_openai_key: str = ""
    azure_openai_deployment: str = "gpt-4o"
    azure_openai_api_version: str = "2024-06-01"
    search_provider: str = "dummy"
    azure_search_endpoint: str = ""
    azure_search_key: str = ""
    azure_search_index: str = "property-index"
    storage_provider: str = "local"
    upload_dir: str = "./uploads"
    azure_blob_connection_string: str = ""
    azure_blob_container: str = "documents"
    auth_provider: str = "local"
    azure_ad_tenant_id: str = ""
    azure_ad_client_id: str = ""
    azure_ad_client_secret: str = ""
    auto_assign_agents: bool = True
    visit_slot_minutes: int = 60
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
