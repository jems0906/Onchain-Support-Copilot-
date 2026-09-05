import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Network = Literal["base", "base-sepolia"]

ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
TX_HASH_RE = re.compile(r"^0x[a-fA-F0-9]{64}$")


class CaseCreate(BaseModel):
    network: Network
    wallet_address: str | None = None
    transaction_hash: str | None = None
    contract_address: str | None = None
    error_message: str = Field(min_length=3, max_length=4000)
    tool_used: str = Field(min_length=2, max_length=128)
    issue_category: str | None = None

    @field_validator("wallet_address", "contract_address")
    @classmethod
    def validate_address_fields(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not ADDRESS_RE.fullmatch(value):
            raise ValueError("must be a valid 20-byte Ethereum address in 0x-prefixed hex format")
        return value

    @field_validator("transaction_hash")
    @classmethod
    def validate_transaction_hash(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not TX_HASH_RE.fullmatch(value):
            raise ValueError("must be a valid 32-byte transaction hash in 0x-prefixed hex format")
        return value


class TriageRequest(CaseCreate):
    pass


class RpcRequest(BaseModel):
    network: Network
    value: str

    @field_validator("value")
    @classmethod
    def validate_rpc_value(cls, value: str) -> str:
        if not (ADDRESS_RE.fullmatch(value) or TX_HASH_RE.fullmatch(value)):
            raise ValueError("must be a valid Base wallet or transaction hash in 0x-prefixed hex format")
        return value


class DraftRequest(BaseModel):
    case: CaseCreate
    triage: dict


class ReviewRequest(BaseModel):
    case_id: str
    status: Literal["accepted", "edited", "rejected"]
    response: str | None = Field(default=None, max_length=12000)
    source: Literal["playbook", "custom"] = "custom"
