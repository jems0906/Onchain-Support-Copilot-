import pytest

from app import onchain


@pytest.mark.asyncio
async def test_verify_network_accepts_base_chain(monkeypatch):
    async def fake_rpc_call(network, method, params):
        assert network == "base"
        assert method == "eth_chainId"
        return "0x2105"

    monkeypatch.setattr(onchain, "rpc_call", fake_rpc_call)
    await onchain.verify_network("base")
