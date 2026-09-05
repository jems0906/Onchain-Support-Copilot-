import pytest

from app import onchain


@pytest.mark.asyncio
async def test_receipt_parses_failed_transaction(monkeypatch):
    async def fake_rpc_call(network, method, params):
        assert network == 'base'
        if method == 'eth_chainId':
            return '0x2105'
        assert method in {'eth_getTransactionReceipt', 'eth_getTransactionByHash'}
        return {'status': '0x0', 'gasUsed': '0x5208', 'blockNumber': '0x10'}

    monkeypatch.setattr(onchain, 'rpc_call', fake_rpc_call)
    result = await onchain.receipt('base', '0x' + '1' * 64)
    assert result['status'] == 'failed'
    assert result['gas_used'] == 21000
    assert result['revert_reason'] is not None


@pytest.mark.asyncio
async def test_code_reports_deployment(monkeypatch):
    async def fake_rpc_call(network, method, params):
        if method == 'eth_chainId':
            return '0x14a34'
        return '0x6000'

    monkeypatch.setattr(onchain, 'rpc_call', fake_rpc_call)
    assert (await onchain.code('base-sepolia', '0x' + '2' * 40))['deployed'] is True


def test_decode_standard_revert_reason():
    reason = 'execution reverted'
    encoded = '0x08c379a0' + f'{32:064x}' + f'{len(reason):064x}' + reason.encode().hex().ljust(64, '0')
    assert onchain.decode_revert_data(encoded) == reason
