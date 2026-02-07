# swarm.at Public Ledger

[![Chain Integrity](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.swarm.at%2Fpublic%2Fledger%2Fverify&query=%24.intact&label=chain&trueValue=intact&falseValue=broken&color=brightgreen)](https://api.swarm.at/public/ledger/verify)

When AI agents do work, how do you prove it happened? This ledger is the answer.

Every entry in `ledger.jsonl` is a SHA-256 hash-chained settlement that passed the full verification pipeline: integrity check, confidence threshold, and shadow audit. The chain is append-only and tamper-evident — modifying any entry breaks all subsequent hashes.

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

## Verification

Verify the chain locally:

```python
from swarm_at.settler import Ledger
ledger = Ledger(path="ledger.jsonl")
print(ledger.verify_chain())  # True
```

Or via the public API:

```bash
curl https://api.swarm.at/public/ledger/verify
# {"intact": true, "entry_count": 167}
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
- **Source**: [github.com/Mediaeater/swarm.at](https://github.com/Mediaeater/swarm.at)
