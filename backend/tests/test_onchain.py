import pytest

from app import onchain


@pytest.mark.asyncio
async def test_receipt_parses_failed_transaction(monkeypatch):
    async def fake_rpc_call(network, method, params):
        assert network == 'base'
        assert method == 'eth_getTransactionReceipt'
        return {'status': '0x0', 'gasUsed': '0x5208', 'blockNumber': '0x10'}

    monkeypatch.setattr(onchain, 'rpc_call', fake_rpc_call)
    result = await onchain.receipt('base', '0x' + '1' * 64)
    assert result['status'] == 'failed'
    assert result['gas_used'] == 21000
    assert result['revert_reason'] is not None


@pytest.mark.asyncio
async def test_code_reports_deployment(monkeypatch):
    async def fake_rpc_call(network, method, params):
        return '0x6000'

    monkeypatch.setattr(onchain, 'rpc_call', fake_rpc_call)
    assert (await onchain.code('base-sepolia', '0x' + '2' * 40))['deployed'] is True
