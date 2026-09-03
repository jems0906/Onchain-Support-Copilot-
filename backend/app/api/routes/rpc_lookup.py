from fastapi import APIRouter, HTTPException
from app.onchain import receipt, balance, code
from app.schemas import RpcRequest

router = APIRouter(prefix="/rpc", tags=["rpc"])

async def lookup(operation, payload):
    try:
        return await operation(payload.network, payload.value)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Base RPC lookup failed: {exc}") from exc

@router.post("/tx-receipt")
async def tx_receipt(payload: RpcRequest):
    return await lookup(receipt, payload)

@router.post("/balance")
async def account_balance(payload: RpcRequest):
    return await lookup(balance, payload)

@router.post("/code")
async def contract_code(payload: RpcRequest):
    return await lookup(code, payload)
