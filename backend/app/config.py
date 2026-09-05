import os


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "y"}


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def get_list_env(name: str, default: str = "*") -> list[str]:
    raw_value = os.getenv(name, default)
    if raw_value is None:
        return []
    values = [item.strip() for item in raw_value.split(',') if item.strip()]
    return values


def validate_environment() -> None:
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env != "production":
        return

    if os.getenv("AUTH_REQUIRED", "false").strip().lower() in {"1", "true", "yes", "on", "y"}:
        if not os.getenv("API_TOKEN", "").strip():
            raise RuntimeError("Production configuration error: API_TOKEN is required when AUTH_REQUIRED=true.")

    if not os.getenv("DATABASE_URL", "").strip():
        raise RuntimeError("Production configuration error: DATABASE_URL is required.")

    if os.getenv("AI_PROVIDER", "mock").strip().lower() == "openai" and not os.getenv("OPENAI_API_KEY", "").strip():
        raise RuntimeError("Production configuration error: OPENAI_API_KEY is required when AI_PROVIDER=openai.")


NETWORKS = {
    "base": {"name": "Base Mainnet", "chain_id": 8453, "rpc_url": "https://mainnet.base.org", "explorer": "https://basescan.org"},
    "base-sepolia": {"name": "Base Sepolia", "chain_id": 84532, "rpc_url": "https://sepolia.base.org", "explorer": "https://sepolia.basescan.org"},
}

APP_NAME = "Onchain Support Copilot"
APP_VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "mock").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
RATE_LIMIT_PER_MINUTE = get_int_env("RATE_LIMIT_PER_MINUTE", 120)
RATE_LIMIT_WINDOW_SECONDS = get_int_env("RATE_LIMIT_WINDOW_SECONDS", 60)
API_TOKEN = os.getenv("API_TOKEN", "")
AUTH_REQUIRED = get_bool_env("AUTH_REQUIRED", False)
CORS_ALLOWED_ORIGINS = get_list_env("CORS_ALLOWED_ORIGINS", "*")


def get_allowed_origins() -> list[str]:
    origins = CORS_ALLOWED_ORIGINS
    return ["*"] if origins == ["*"] else origins


validate_environment()
