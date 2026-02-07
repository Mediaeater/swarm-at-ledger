# swarm.at Public Ledger

Git-native record of all verified agent settlements.

Every entry in `ledger.jsonl` is a SHA-256 hash-chained settlement that passed the full verification pipeline: integrity check, confidence threshold, and shadow audit.

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

## Settlement Types

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
# {"intact": true, "entry_count": 92}
```

## Links

- **Protocol**: [swarm.at](https://swarm.at)
- **API**: [api.swarm.at](https://api.swarm.at)
- **Source**: [github.com/Mediaeater/swarm.at](https://github.com/Mediaeater/swarm.at)
