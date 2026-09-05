import httpx
from app.config import NETWORKS

async def rpc_call(network: str, method: str, params: list):
    async with httpx.AsyncClient(timeout=8) as client:
        response = await client.post(NETWORKS[network]["rpc_url"], json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
        response.raise_for_status()
        body = response.json()
        if "error" in body:
            raise ValueError(body["error"].get("message", "RPC error"))
        return body.get("result")


async def verify_network(network: str):
    chain_id = await rpc_call(network, "eth_chainId", [])
    expected = hex(NETWORKS[network]["chain_id"])
    if chain_id.lower() != expected.lower():
        raise ValueError(f"RPC chain mismatch: expected {expected}, received {chain_id}")


def decode_revert_data(data: str | None) -> str | None:
    if not data or data == "0x":
        return None
    if data.startswith("0x08c379a0") and len(data) >= 138:
        try:
            offset = int(data[10:74], 16)
            length_start = 10 + offset * 2
            length = int(data[length_start:length_start + 64], 16)
            data_start = length_start + 64
            return bytes.fromhex(data[data_start:data_start + length * 2]).decode("utf-8", errors="replace")
        except (ValueError, UnicodeDecodeError):
            return "Contract returned Error(string)"
    if data.startswith("0x4e487b71"):
        return "Contract panicked during execution"
    return "Contract returned a custom error"

async def receipt(network: str, tx_hash: str):
    await verify_network(network)
    value = await rpc_call(network, "eth_getTransactionReceipt", [tx_hash])
    if value is None:
        return {"found": False, "status": "pending-or-unknown"}
    status = "success" if value.get("status") == "0x1" else "failed"
    revert_reason = None
    if status == "failed":
        try:
            transaction = await rpc_call(network, "eth_getTransactionByHash", [tx_hash])
            revert_data = await rpc_call(network, "eth_call", [{"from": transaction.get("from"), "to": transaction.get("to"), "data": transaction.get("input", "0x"), "value": transaction.get("value", "0x0")}, value.get("blockNumber", "latest")])
            revert_reason = decode_revert_data(revert_data)
        except Exception:
            revert_reason = "Revert reason unavailable from public RPC"
    return {"found": True, "status": status, "gas_used": int(value.get("gasUsed", "0x0"), 16), "block_number": int(value.get("blockNumber", "0x0"), 16), "revert_reason": revert_reason, "receipt": value}

async def balance(network: str, address: str):
    await verify_network(network)
    value = await rpc_call(network, "eth_getBalance", [address, "latest"])
    return {"wei": value, "eth": int(value, 16) / 10**18}

async def code(network: str, address: str):
    await verify_network(network)
    value = await rpc_call(network, "eth_getCode", [address, "latest"])
    return {"code": value, "deployed": value not in (None, "0x")}
