from typing import Literal
from pydantic import BaseModel, Field

Network = Literal["base", "base-sepolia"]

class CaseCreate(BaseModel):
    network: Network
    wallet_address: str | None = None
    transaction_hash: str | None = None
    contract_address: str | None = None
    error_message: str = Field(min_length=3, max_length=4000)
    tool_used: str
    issue_category: str | None = None

class TriageRequest(CaseCreate):
    pass

class RpcRequest(BaseModel):
    network: Network
    value: str

class DraftRequest(BaseModel):
    case: CaseCreate
    triage: dict

class ReviewRequest(BaseModel):
    case_id: str
    status: Literal["accepted", "edited", "rejected"]
    response: str | None = None
