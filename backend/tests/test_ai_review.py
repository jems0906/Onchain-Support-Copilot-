import pytest

from app.ai_provider import generate_draft


@pytest.mark.asyncio
async def test_mock_draft_is_playbook_grounded(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "mock")
    playbook = {"title": "Wallet connection", "summary": "Reconnect the wallet.", "steps": ["Select Base"], "citation": "wallet playbook"}
    draft, provider = await generate_draft({"network": "base", "tool_used": "MetaMask", "error_message": "wallet"}, {"category": "wallet-connection"}, playbook)
    assert provider == "approved-playbook-mock"
    assert "Select Base" in draft
