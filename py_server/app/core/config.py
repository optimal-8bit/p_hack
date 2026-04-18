from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "pHack API"
    app_env: str = "dev"
    api_prefix: str = "/api/v1"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "phack"
    jwt_secret_key: str = "change-this-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    google_client_id: str = ""
    ai_request_timeout_seconds: int = 90
    ai_temperature: float = 0.2
    ai_max_tokens: int = 512
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openai/gpt-4o-mini"
    google_ai_studio_api_key: str = ""
    google_ai_studio_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    google_ai_studio_model: str = "gemini-1.5-flash"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""
    cloudinary_secure: bool = True
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    google_service_account_file: str = ""
    google_workspace_delegated_user: str = ""
    google_calendar_id: str = "primary"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = ""
    neo4j_database: str = "neo4j"
    rag_chunk_label: str = "RagChunk"
    rag_vector_index_name: str = "rag_chunk_embedding"
    rag_chunk_size: int = 900
    rag_chunk_overlap: int = 120
    rag_top_k: int = 5
    rag_cache_ttl_seconds: int = 300
    rag_retry_attempts: int = 3
    rag_retry_base_delay_seconds: float = 0.5
    rag_embedding_provider_order: str = "google_ai_studio,openrouter,ollama"
    rag_google_embedding_model: str = "text-embedding-004"
    rag_openrouter_embedding_model: str = "openai/text-embedding-3-small"
    rag_ollama_embedding_model: str = "nomic-embed-text"
    rag_generation_provider_order: str = "google_ai_studio,openrouter,ollama"
    rag_generation_temperature: float = 0.2
    rag_generation_max_tokens: int = 512

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
