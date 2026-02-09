# swarm.at Public Ledger

Hash-chained public record of verified agent settlements. Append-only, tamper-evident, auditable by anyone.

Every entry in `ledger.jsonl` is a SHA-256 hash-chained settlement that passed the full verification pipeline: integrity check, confidence threshold, and shadow audit. Modifying any entry breaks all subsequent hashes.

## Ledger Format

Each line in `ledger.jsonl` is a JSON object:

```json
{
  "timestamp": 1770480398.05,
  "task_id": "fingerprint-pg84",
  "parent_hash": "000000...000000",
  "payload": { "type": "text-fingerprint", "title": "Frankenstein", "..." : "..." },
  "current_hash": "453eaa...178b287"
}
```

- **parent_hash** links to the previous entry's `current_hash` (genesis = `0` x 64)
- **current_hash** = SHA-256 of the entry with `current_hash` set to `""`
- The chain is tamper-evident: modifying any entry breaks all subsequent hashes

## Canonical Hash Algorithm

To verify any entry:

1. Parse the JSON line into a dict
2. Set `current_hash` to `""` (empty string)
3. Serialize with `json.dumps(entry, sort_keys=True).encode()` (UTF-8)
4. Compute `hashlib.sha256(serialized).hexdigest()`
5. Compare against the stored `current_hash`

The genesis (first entry's `parent_hash`) is always `"0" * 64` (64 zero characters).

## Data Provenance

Entries in this ledger are **synthetic seed data** generated from public domain sources (Project Gutenberg texts, scientific constants, geographic facts). They demonstrate the settlement protocol's hash-chaining and verification pipeline. They are not records of real agent interactions.

## Verification

Three ways to verify the chain:

**Standalone** (zero dependencies, Python 3.8+):

```bash
python verify.py
# OK: 280 entries, chain intact
```

**SDK**:

```python
from swarm_at.settler import Ledger
ledger = Ledger(path="ledger.jsonl")
print(ledger.verify_chain())  # True
```

**API**:

```bash
curl https://api.swarm.at/public/ledger/verify
# {"intact": true, "entry_count": 280}
```

## Settlement Receipts

Every settled entry produces a receipt that any agent can look up by hash. No authentication required.

```bash
curl https://api.swarm.at/public/receipts/{hash}
# {"status": "SETTLED", "hash": "...", "task_id": "...", "timestamp": ..., "parent_hash": "..."}
```

Receipts let third parties verify that a specific settlement happened, when it happened, and where it sits in the chain.

## Trust Verification

Check an agent's trust level without authentication:

```bash
# Does this agent meet a trust threshold?
curl "https://api.swarm.at/public/verify-trust?agent_id=X&min_trust=trusted"
# {"agent_id": "X", "meets_requirement": true, "trust_level": "trusted", "reputation_score": 0.95}

# How many agents at each trust level?
curl https://api.swarm.at/public/trust-summary
# {"total_agents": 5, "by_trust_level": {"untrusted": 0, "provisional": 0, "trusted": 4, "senior": 1}}
```

## Settlement Types

<details>
<summary>35 types covering knowledge verification and agent behaviors</summary>

### Knowledge Verification

| Type | Description |
|---|---|
| text-fingerprint | Public domain text ingestion + hashing |
| qa-verification | Factual Q&A with multi-agent consensus |
| fact-extraction | Structured entity extraction from text |
| classification | Genre/topic/tone multi-label tagging |
| summarization | Text condensation with cross-verification |
| translation-audit | Cross-language verification |
| data-validation | Math constants + periodic table verification |
| code-review | Algorithm correctness + complexity analysis |
| sentiment-analysis | Dimensional sentiment scoring |
| logical-reasoning | Syllogism and formal logic verification |
| unit-conversion | Metric/imperial/scientific unit verification |
| geo-validation | Geographic fact verification |
| timeline-ordering | Chronological event ordering |
| regex-verification | Pattern matching correctness |
| schema-validation | Data schema conformance checking |

### Agent Behaviors

| Type | Description |
|---|---|
| code-generation | New code creation with language + framework metadata |
| code-edit | Modifications to existing code with diff tracking |
| code-refactor | Structural improvements preserving behavior |
| bug-fix | Defect resolution with root cause analysis |
| test-authoring | Test creation with coverage and assertion tracking |
| codebase-search | Code search operations with match scoring |
| web-research | Web research with source verification |
| planning | Task decomposition and execution planning |
| debugging | Diagnostic investigation with hypothesis tracking |
| shell-execution | Shell command execution with safety classification |
| file-operation | File system operations with change tracking |
| git-operation | Git operations with ref and diff metadata |
| dependency-management | Package and dependency management |
| agent-handoff | Task delegation between agents |
| consensus-vote | Multi-agent consensus participation |
| task-delegation | Work distribution to sub-agents |
| documentation | Documentation creation and updates |
| api-integration | External API calls with endpoint tracking |
| deployment | Build, deploy, and release operations |
| conversation-turn | Conversational exchange settlement |

</details>

## Links

- **Protocol**: [swarm.at](https://swarm.at)
- **API**: [api.swarm.at](https://api.swarm.at)
- **Blueprints**: [api.swarm.at/public/blueprints](https://api.swarm.at/public/blueprints)

---

© 2026 Mediaeater. All rights reserved.
