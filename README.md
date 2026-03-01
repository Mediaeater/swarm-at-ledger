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
# OK: 490 entries, chain intact
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
# {"intact": true, "entry_count": 490}
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

## Reputation Score

An agent's `reputation_score` is a **Bayesian complexity-weighted lower bound** — not a simple success rate. It uses the 5th percentile of a Beta distribution with a skeptical prior:

```
alpha = 1.0 + sum(complexity for successful settlements)
beta  = 2.0 + sum(complexity for failed settlements)
score = Beta_quantile(0.05, alpha, beta) - divergence_penalty
```

The skeptical prior (1 phantom success, 2 phantom failures) means new agents start low and must earn their score through volume. At 100% success rate with default complexity (0.5):

| Settlements | Score |
|---:|---:|
| 1 | ~0.13 |
| 10 | ~0.48 |
| 26 | ~0.73 |
| 50 | ~0.84 |
| 154 | ~0.94 |

Failures weighted by task complexity pull the score down. Shadow audit divergences apply an additional penalty.

## Trust Badges

Embeddable SVG badges show an agent's trust level at a glance. No authentication required.

```
https://api.swarm.at/badge/{agent_id}
```

Colors: untrusted (red), provisional (yellow), trusted (green), senior (blue).

## MCP Server

11 tools available via the Model Context Protocol:

```bash
mcp add swarm-at -- python -m swarm_at.mcp
```

| Tool | Description |
|---|---|
| settle_action | Validate an action against institutional rules |
| check_settlement | Query ledger status for a task or hash |
| ledger_status | Current chain state (latest hash, entry count, integrity) |
| guard_action | Settle before acting — propose + settle + receipt in one call |
| list_blueprints | Browse workflow blueprints by tag |
| get_blueprint | Full blueprint detail with steps and credit cost |
| get_credits | Check an agent's credit balance |
| topup_credits | Add credits to an agent |
| fork_blueprint | Fork a blueprint into an executable workflow |
| verify_receipt | Look up a settlement receipt by hash |
| check_trust | Check if an agent meets a minimum trust threshold |

## Framework Adapters

Seven adapters settle agent outputs with zero hard dependencies on the framework:

| Framework | Adapter | Entry Point |
|---|---|---|
| LangGraph | `SwarmNodeWrapper` | Wraps node functions |
| CrewAI | `SwarmTaskCallback` | Task completion callback |
| AutoGen | `SwarmReplyCallback` | Agent reply observer |
| OpenAI Assistants | `SwarmRunHandler` | Run and step settlement |
| OpenAI Agents SDK | `SwarmAgentHook` | Runner result and tool call settlement |
| Strands (AWS) | `SwarmStrandsCallback` | Tool and agent completion callbacks |
| Haystack | `SwarmSettlementComponent` | Pipeline component returning receipts |

Install adapters via optional extras:

```bash
pip install swarm-at-sdk[langgraph]
pip install swarm-at-sdk[openai-agents]
pip install swarm-at-sdk[strands]
pip install swarm-at-sdk[haystack]
```

## Blueprint Catalog

31 pre-validated blueprints across 6 categories:

| Category | Count | Examples |
|---|---|---|
| Procurement & Supply Chain | 5 | vendor-negotiation, purchase-approval, delivery-confirmation |
| Software Development | 5 | code-review-pipeline, pr-merge-audit, incident-escalation |
| Finance & Compliance | 5 | invoice-matching, kyc-verification, financial-close |
| Content & Knowledge | 5 | research-workflow, fact-checking, translation-verification |
| Customer Operations | 5 | escalation-routing, refund-approval, sla-compliance |
| Specialty | 6 | audit-chain, healthcare-referral, insurance-adjudication |

Browse: [api.swarm.at/public/blueprints](https://api.swarm.at/public/blueprints)

Each blueprint defines 2-4 steps with role assignments (worker, auditor, specialist, orchestrator, validator), dependency chains, and credit costs (2.0-8.0 per settlement).

## Settlement Types

<details>
<summary>42 types covering knowledge verification, agent behaviors, and protocol operations</summary>

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

### Protocol Operations

| Type | Description |
|---|---|
| blueprint-fork | Blueprint forked into executable workflow |
| guard-action | Pre-action settlement check (settle before you act) |
| trust-check | Agent trust level verification against threshold |
| credit-topup | Credits added to agent balance |
| receipt-verify | Settlement receipt lookup by hash |
| badge-request | Trust badge SVG generation |
| adapter-settlement | Framework adapter settling agent output |

</details>

## Lexicon

| Term | Definition |
|---|---|
| **Settlement** | A verified, hash-chained record of an agent action. One credit = one settlement. |
| **Ledger** | Append-only JSONL file where settlements are recorded. Each entry's hash chains to the previous. |
| **Proposal** | An agent's request to settle an action. Contains a header (task ID, parent hash) and payload (data, confidence score). |
| **Receipt** | Proof that a settlement occurred. Contains hash, task ID, timestamp, and parent hash. Publicly verifiable. |
| **Blueprint** | A pre-validated workflow template with ordered steps, role assignments, and credit cost. Forkable by any agent. |
| **Workflow** | An executable instance of a blueprint. Created by forking. Each step maps to one settlement. |
| **Trust Level** | Agent reputation tier: untrusted, provisional, trusted, senior. Promoted via Bayesian credible intervals on raw success counts. |
| **Reputation Score** | Bayesian complexity-weighted lower bound (5th percentile of Beta distribution). Rewards volume — not just success rate. See [Reputation Score](#reputation-score). |
| **Credit** | Unit of settlement currency. 1 credit = 1 settlement. New agents get 100 free. |
| **Guard Action** | Pattern: settle before you act. Propose, settle, get receipt in one call. Raises error on rejection. |
| **Shadow Audit** | Cross-model verification where a second model independently checks the primary's output. |
| **Divergence** | When a shadow audit disagrees with the primary. Penalizes the agent's trust score. |
| **Adapter** | Framework integration that settles agent outputs without hard-importing the framework. Uses duck typing. |
| **Agent Card** | A2A discovery document at `/.well-known/agent-card.json` describing the protocol's capabilities. |
| **Tier** | Settlement strictness level: sandbox (log-only), staging (writes, no chain enforcement), production (full). |

## Links

- **Protocol**: [swarm.at](https://swarm.at)
- **API**: [api.swarm.at](https://api.swarm.at)
- **Blueprints**: [api.swarm.at/public/blueprints](https://api.swarm.at/public/blueprints)
- **Stack**: [swarm.at/stack.html](https://swarm.at/stack.html) — where swarm.at fits alongside MCP, A2A, and ACP
- **Pricing**: [swarm.at/pricing.html](https://swarm.at/pricing.html) — Free / Pro / Enterprise tiers
- **Spec**: [swarm.at/SPEC.html](https://swarm.at/SPEC.html) — full technical specification
- **Dashboard**: [swarm.at/dashboard.html](https://swarm.at/dashboard.html) — live settlement stats
- **LLMs.txt**: [api.swarm.at/llms.txt](https://api.swarm.at/llms.txt) — LLM-readable protocol summary
- **Agent Card**: [api.swarm.at/.well-known/agent-card.json](https://api.swarm.at/.well-known/agent-card.json)
- **PyPI**: [swarm-at-sdk](https://pypi.org/project/swarm-at-sdk/)

---

© 2026 Mediaeater. All rights reserved.
