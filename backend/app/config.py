import os

NETWORKS = {
    "base": {"name": "Base Mainnet", "chain_id": 8453, "rpc_url": "https://mainnet.base.org", "explorer": "https://basescan.org"},
    "base-sepolia": {"name": "Base Sepolia", "chain_id": 84532, "rpc_url": "https://sepolia.base.org", "explorer": "https://sepolia.basescan.org"},
}
DATABASE_URL = os.getenv("DATABASE_URL", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
