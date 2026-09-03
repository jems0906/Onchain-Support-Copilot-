from fastapi import APIRouter, HTTPException
from app.knowledge import PLAYBOOKS

router = APIRouter(prefix="/kb", tags=["knowledge-base"])

@router.get("")
def list_playbooks():
    return {"items": list(PLAYBOOKS.values())}

@router.get("/{topic}")
def get_playbook(topic: str):
    if topic not in PLAYBOOKS:
        raise HTTPException(status_code=404, detail="Playbook not found")
    return PLAYBOOKS[topic]
