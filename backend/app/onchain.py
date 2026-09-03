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

async def receipt(network: str, tx_hash: str):
    value = await rpc_call(network, "eth_getTransactionReceipt", [tx_hash])
    if value is None:
        return {"found": False, "status": "pending-or-unknown"}
    status = "success" if value.get("status") == "0x1" else "failed"
    return {"found": True, "status": status, "gas_used": int(value.get("gasUsed", "0x0"), 16), "block_number": int(value.get("blockNumber", "0x0"), 16), "revert_reason": None if status == "success" else "Revert reason requires replaying the transaction call.", "receipt": value}

async def balance(network: str, address: str):
    value = await rpc_call(network, "eth_getBalance", [address, "latest"])
    return {"wei": value, "eth": int(value, 16) / 10**18}

async def code(network: str, address: str):
    value = await rpc_call(network, "eth_getCode", [address, "latest"])
    return {"code": value, "deployed": value not in (None, "0x")}
