from fastapi import APIRouter
from app.onchain import receipt
from app.schemas import TriageRequest
from app.triage import triage_case

router = APIRouter(prefix="/triage", tags=["triage"])

@router.post("")
async def run_triage(payload: TriageRequest):
    data = payload.model_dump()
    result = triage_case(data)
    result["rpc_lookup"] = None
    if data.get("transaction_hash"):
        try:
            result["rpc_lookup"] = await receipt(data["network"], data["transaction_hash"])
            if result["rpc_lookup"]["status"] == "failed" and result["category"] == "general":
                result["category"] = "transaction-reverted"
        except Exception as error:
            result["rpc_lookup"] = {"status": "unavailable", "error": str(error)}
    return result
