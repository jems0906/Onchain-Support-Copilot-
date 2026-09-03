import re

TX_HASH = re.compile(r"^0x[a-fA-F0-9]{64}$")
ADDRESS = re.compile(r"^0x[a-fA-F0-9]{40}$")

RULES = [
    ("security", ["scam", "phishing", "stolen", "drain", "fake"]),
    ("bridge-delay", ["bridge", "pending", "deposit", "withdrawal", "l1", "l2"]),
    ("rpc-error", ["rpc", "timeout", "429", "connection", "endpoint", "rate limit"]),
    ("gas-estimation", ["gas", "underpriced", "estimation", "insufficient funds"]),
    ("wallet-connection", ["wallet", "connect", "metamask", "coinbase wallet", "wrong network"]),
    ("contract-verification", ["verify", "verification", "basescan", "source code"]),
    ("contract-deployment", ["deploy", "deployment", "bytecode", "constructor"]),
    ("faucet", ["faucet", "test eth", "testnet funds"]),
    ("transaction-reverted", ["revert", "reverted", "failed", "execution reverted"]),
]


def triage_case(payload: dict) -> dict:
    error = payload.get("error_message", "").lower()
    findings = []
    if payload.get("transaction_hash") and not TX_HASH.match(payload["transaction_hash"]):
        findings.append({"code": "invalid-tx-hash", "severity": "high", "title": "Invalid transaction hash", "detail": "A transaction hash must be 0x followed by 64 hexadecimal characters."})
    if payload.get("wallet_address") and not ADDRESS.match(payload["wallet_address"]):
        findings.append({"code": "invalid-wallet", "severity": "medium", "title": "Wallet address format looks invalid", "detail": "Check that the address is a 42-character hexadecimal EVM address."})
    if payload.get("contract_address") and not ADDRESS.match(payload["contract_address"]):
        findings.append({"code": "invalid-contract", "severity": "medium", "title": "Contract address format looks invalid", "detail": "Check that the address is a 42-character hexadecimal EVM address."})
    matches = [category for category, terms in RULES if any(term in error for term in terms)]
    category = matches[0] if matches else payload.get("issue_category") or "general"
    if category != "general":
        findings.append({"code": category, "severity": "medium", "title": category.replace("-", " ").title(), "detail": f"Signals in the error message match the {category.replace('-', ' ')} playbook."})
    if payload.get("network") not in ("base", "base-sepolia"):
        findings.append({"code": "unknown-network", "severity": "high", "title": "Unsupported network", "detail": "Use Base Mainnet or Base Sepolia."})
    network_terms = {"base": ["8453", "mainnet"], "base-sepolia": ["84532", "sepolia"]}
    selected_terms = network_terms.get(payload.get("network"), [])
    other_terms = [term for network, terms in network_terms.items() if network != payload.get("network") for term in terms]
    has_other_network = any(re.search(rf"(?<!\d){re.escape(term)}(?!\d)", error) for term in other_terms)
    has_selected_network = any(re.search(rf"(?<!\d){re.escape(term)}(?!\d)", error) for term in selected_terms)
    if has_other_network and not has_selected_network:
        findings.append({"code": "network-mismatch", "severity": "high", "title": "Possible network mismatch", "detail": "The error references a different Base network than the selected network."})
    return {"category": category, "confidence": min(0.98, 0.55 + (0.12 * len(findings))), "findings": findings, "next_steps": next_steps(category)}


def next_steps(category: str) -> list[str]:
    return {
        "transaction-reverted": ["Inspect the receipt and contract logs", "Compare the call inputs with the contract requirements", "Retry only after confirming the state-dependent preconditions"],
        "rpc-error": ["Check endpoint health and HTTP status", "Retry with exponential backoff", "Use the network-specific Base endpoint"],
        "bridge-delay": ["Confirm the source transaction succeeded", "Check the bridge status and expected settlement window", "Do not resubmit while the original message is pending"],
        "security": ["Do not ask for private keys or seed phrases", "Preserve transaction and address evidence", "Escalate to the security response workflow"],
    }.get(category, ["Confirm the selected network", "Collect the relevant transaction or contract identifier", "Follow the matched playbook and document the outcome"])
