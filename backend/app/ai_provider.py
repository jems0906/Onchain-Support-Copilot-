import json
import os

import httpx


async def generate_draft(case: dict, triage: dict, playbook: dict) -> tuple[str, str]:
    provider = os.getenv("AI_PROVIDER", "mock").lower()
    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        try:
            return await _openai_draft(case, triage, playbook), "openai"
        except (httpx.HTTPError, KeyError, ValueError):
            pass
    steps = " ".join(f"{index + 1}) {step}" for index, step in enumerate(playbook["steps"]))
    draft = f"Thanks for the detailed report. Based on the available signals, this looks like {playbook['title'].lower()}. {playbook['summary']} Recommended checks: {steps} Please share the relevant hash or address if the issue persists."
    return draft, "approved-playbook-mock"


async def _openai_draft(case: dict, triage: dict, playbook: dict) -> str:
    allowed_steps = "\n".join(f"- {step}" for step in playbook["steps"])
    prompt = {
        "case": {"network": case["network"], "tool_used": case["tool_used"], "error_message": case["error_message"]},
        "triage": triage,
        "playbook": {"title": playbook["title"], "summary": playbook["summary"], "allowed_steps": allowed_steps},
    }
    body = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": "Write a concise support draft using only the supplied playbook. Do not invent steps, request secrets, or claim certainty. Return plain text only."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
    }
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()