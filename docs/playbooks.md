# Approved Playbooks

- **Wallet connection:** verify chain ID, clear stale sessions, reconnect, and never request secrets.
- **Failed transaction:** inspect receipt status, gas used, logs, and contract preconditions.
- **RPC errors:** verify endpoint and network, retry with backoff, and avoid duplicate submissions.
- **Bridge delay:** confirm source success, check bridge status, and retain the source hash.
- **Contract deployment and verification:** confirm deployed bytecode, compiler settings, constructor args, and Basescan network.
- **Security:** preserve evidence, warn against further transfers, and escalate.
- **Faucets:** use Base Sepolia only for test funds and never promise mainnet assets.
