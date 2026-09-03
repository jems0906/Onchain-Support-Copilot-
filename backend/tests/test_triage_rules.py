from app.triage import triage_case

def test_invalid_hash_is_flagged():
    result = triage_case({"network": "base", "transaction_hash": "0x123", "error_message": "execution reverted"})
    assert result["category"] == "transaction-reverted"
    assert any(item["code"] == "invalid-tx-hash" for item in result["findings"])

def test_rpc_error_category():
    result = triage_case({"network": "base-sepolia", "error_message": "RPC timeout while connecting"})
    assert result["category"] == "rpc-error"

def test_network_mismatch_is_flagged():
    result = triage_case({"network": "base", "error_message": "chain id 84532 rejected"})
    assert any(item["code"] == "network-mismatch" for item in result["findings"])
