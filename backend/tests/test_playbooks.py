from app.knowledge import PLAYBOOKS


def test_required_support_playbooks_are_available():
    for category in ("wallet-connection", "transaction-reverted", "rpc-error", "bridge-delay", "contract-deployment", "contract-verification", "security", "faucet"):
        assert category in PLAYBOOKS
        assert PLAYBOOKS[category]["steps"]
