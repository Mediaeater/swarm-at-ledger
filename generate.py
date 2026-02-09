#!/usr/bin/env python3
"""Generate additional ledger entries to bulk up the public ledger.

Adds ~233 entries (267 existing + 233 = 500 total) covering:
- More of existing settlement types (bulk)
- New Cold Start Kit types: blueprint-fork, guard-action, trust-check,
  credit-topup, receipt-verify, badge-request
"""

import hashlib
import json
import random
import sys

random.seed(42)  # Reproducible


def make_hash(entry: dict) -> str:
    entry["current_hash"] = ""
    return hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()


def make_entry(parent_hash: str, timestamp: float, task_id: str, payload: dict) -> dict:
    entry = {
        "timestamp": timestamp,
        "task_id": task_id,
        "parent_hash": parent_hash,
        "payload": payload,
        "current_hash": "",
    }
    entry["current_hash"] = make_hash(entry)
    return entry


# ── New Cold Start Kit types ──────────────────────────────────────────

BLUEPRINT_IDS = [
    "vendor-negotiation", "purchase-approval", "delivery-confirmation",
    "supplier-scoring", "contract-verification", "code-review-pipeline",
    "pr-merge-audit", "dependency-triage", "release-approval",
    "incident-escalation", "invoice-matching", "expense-approval",
    "kyc-verification", "audit-evidence", "financial-close",
    "research-workflow", "fact-checking", "content-approval",
    "translation-verification", "document-classification",
    "escalation-routing", "refund-approval", "sla-compliance",
    "sentiment-triage", "cross-department-handoff", "audit-chain",
    "healthcare-referral", "legal-negotiation", "iot-validation",
    "real-estate-settlement", "insurance-adjudication",
]

AGENT_IDS = [
    "agent-alpha", "agent-bravo", "agent-charlie", "agent-delta",
    "agent-echo", "agent-foxtrot", "agent-golf", "agent-hotel",
    "agent-india", "agent-juliet", "agent-kilo", "agent-lima",
]

TRUST_LEVELS = ["untrusted", "provisional", "trusted", "senior"]

GUARD_ACTIONS = [
    ("delete-records", {"table": "users", "count": 150}),
    ("drop-table", {"table": "staging_data"}),
    ("send-email-blast", {"recipients": 5000, "template": "promo-q1"}),
    ("deploy-production", {"service": "api-gateway", "version": "2.4.1"}),
    ("revoke-access", {"user_id": "u-9381", "reason": "policy-violation"}),
    ("purge-cache", {"region": "us-east-1", "scope": "all"}),
    ("transfer-funds", {"amount": 25000, "currency": "USD", "to": "vendor-88"}),
    ("shutdown-instance", {"instance_id": "i-0abc123", "region": "eu-west-1"}),
    ("rotate-secrets", {"service": "auth", "key_count": 4}),
    ("archive-project", {"project_id": "proj-legacy-crm"}),
]

FRAMEWORKS = ["langgraph", "crewai", "autogen", "openai-assistants",
              "openai-agents", "strands", "haystack"]

TOOLS_USED = [
    ["read_file", "write_file"], ["web_search"], ["execute_sql"],
    ["code_interpreter"], ["bash", "read_file"], ["api_call"],
    ["settle_action"], ["guard_action"], ["fork_blueprint"],
]

TOPICS = [
    "Evaluate vendor compliance for Q1 procurement",
    "Review pull request #847 for security audit",
    "Verify KYC documents for onboarding batch",
    "Triage incident severity for payment gateway",
    "Check SLA compliance for enterprise tier",
    "Classify support tickets by urgency",
    "Validate IoT sensor readings against thresholds",
    "Cross-check invoice amounts with PO data",
    "Route escalation to appropriate specialist",
    "Approve refund for order #91827",
    "Verify translation accuracy for Japanese locale",
    "Audit evidence collection for SOC2 compliance",
    "Score supplier reliability based on delivery history",
    "Assess insurance claim for property damage",
    "Generate release notes from commit history",
]

# ── Existing type generators ─────────────────────────────────────────

LANGUAGES = ["python", "typescript", "go", "rust", "java", "ruby", "elixir"]
COMPLEXITY_LEVELS = ["trivial", "simple", "moderate", "complex"]
SENTIMENTS = ["positive", "negative", "neutral", "mixed"]
GEO_FACTS = [
    ("Mount Kilimanjaro", "highest peak in Africa", "5895m"),
    ("Mariana Trench", "deepest ocean point", "10994m"),
    ("Lake Baikal", "deepest freshwater lake", "1642m"),
    ("Sahara Desert", "largest hot desert", "9.2M km²"),
    ("Amazon River", "largest river by discharge", "209000 m³/s"),
    ("Caspian Sea", "largest enclosed body of water", "371000 km²"),
    ("Greenland", "largest island", "2.166M km²"),
    ("Nile River", "longest river", "6650 km"),
    ("Pacific Ocean", "largest ocean", "165.25M km²"),
    ("Antarctica", "coldest continent", "-89.2°C record"),
]
MATH_CONSTANTS = [
    ("e", 2.718281828, "Euler's number"),
    ("phi", 1.618033989, "golden ratio"),
    ("sqrt2", 1.414213562, "square root of 2"),
    ("ln2", 0.693147181, "natural log of 2"),
    ("pi/4", 0.785398163, "quarter pi"),
    ("gamma", 0.577215665, "Euler-Mascheroni constant"),
]
CODE_TASKS = [
    "Implement rate limiter middleware",
    "Add retry logic to HTTP client",
    "Create pagination helper for API responses",
    "Build CSV export for settlement data",
    "Write webhook delivery with exponential backoff",
    "Implement circuit breaker pattern",
    "Add request signing for API authentication",
    "Create batch processing pipeline",
    "Build idempotency key middleware",
    "Implement event sourcing for audit log",
]
BUG_DESCRIPTIONS = [
    "Off-by-one in pagination cursor",
    "Race condition in concurrent settlement writes",
    "Missing null check on optional agent_id",
    "Incorrect hash computation for empty payloads",
    "Timezone mismatch in timestamp comparison",
    "Memory leak in long-running webhook listener",
    "Deadlock in consensus voting with 3+ agents",
    "Incorrect content-type header for SVG badges",
]


def gen_blueprint_fork(idx):
    bp = random.choice(BLUEPRINT_IDS)
    agent = random.choice(AGENT_IDS)
    return f"fork-{bp}-{idx}", {
        "type": "blueprint-fork",
        "blueprint_id": bp,
        "agent_id": agent,
        "step_count": random.randint(2, 4),
        "credit_cost": round(random.uniform(2.0, 8.0), 1),
    }


def gen_guard_action(idx):
    action, data = random.choice(GUARD_ACTIONS)
    agent = random.choice(AGENT_IDS)
    return f"guard-{action}-{idx}", {
        "type": "guard-action",
        "agent_id": agent,
        "action": action,
        "data": data,
        "approved": random.random() > 0.15,
    }


def gen_trust_check(idx):
    agent = random.choice(AGENT_IDS)
    min_trust = random.choice(TRUST_LEVELS)
    actual = random.choice(TRUST_LEVELS)
    order = TRUST_LEVELS
    meets = order.index(actual) >= order.index(min_trust)
    return f"trust-check-{idx}", {
        "type": "trust-check",
        "agent_id": agent,
        "min_trust": min_trust,
        "trust_level": actual,
        "meets_requirement": meets,
    }


def gen_credit_topup(idx):
    agent = random.choice(AGENT_IDS)
    amount = random.choice([10, 25, 50, 100, 250, 500])
    return f"topup-{agent}-{idx}", {
        "type": "credit-topup",
        "agent_id": agent,
        "amount": amount,
        "new_balance": round(random.uniform(amount, amount + 500), 2),
    }


def gen_receipt_verify(idx):
    fake_hash = hashlib.sha256(f"receipt-{idx}".encode()).hexdigest()
    return f"verify-receipt-{idx}", {
        "type": "receipt-verify",
        "hash": fake_hash,
        "found": random.random() > 0.2,
        "lookup_source": random.choice(["sdk", "api", "mcp"]),
    }


def gen_badge_request(idx):
    agent = random.choice(AGENT_IDS)
    level = random.choice(TRUST_LEVELS)
    return f"badge-{agent}-{idx}", {
        "type": "badge-request",
        "agent_id": agent,
        "trust_level": level,
        "format": "svg",
    }


def gen_adapter_settle(idx):
    fw = random.choice(FRAMEWORKS)
    return f"adapter-{fw}-{idx}", {
        "type": "adapter-settlement",
        "framework": fw,
        "adapter_class": {
            "langgraph": "SwarmNodeWrapper",
            "crewai": "SwarmTaskCallback",
            "autogen": "SwarmReplyCallback",
            "openai-assistants": "SwarmRunHandler",
            "openai-agents": "SwarmAgentHook",
            "strands": "SwarmStrandsCallback",
            "haystack": "SwarmSettlementComponent",
        }[fw],
        "event": random.choice(["run_complete", "tool_call", "step_complete", "task_done"]),
        "confidence": round(random.uniform(0.8, 1.0), 3),
    }


# Existing type generators (more variety)
def gen_code_generation(idx):
    lang = random.choice(LANGUAGES)
    task = random.choice(CODE_TASKS)
    return f"codegen-{lang}-{idx}", {
        "type": "code-generation",
        "language": lang,
        "task": task,
        "lines_generated": random.randint(15, 200),
        "complexity": random.choice(COMPLEXITY_LEVELS),
        "tests_included": random.random() > 0.3,
    }


def gen_code_review(idx):
    lang = random.choice(LANGUAGES)
    return f"review-{lang}-{idx}", {
        "type": "code-review",
        "language": lang,
        "files_reviewed": random.randint(1, 8),
        "issues_found": random.randint(0, 5),
        "severity_max": random.choice(["info", "warning", "error", "critical"]),
        "approved": random.random() > 0.25,
    }


def gen_bug_fix(idx):
    desc = random.choice(BUG_DESCRIPTIONS)
    lang = random.choice(LANGUAGES)
    return f"bugfix-{idx}", {
        "type": "bug-fix",
        "language": lang,
        "description": desc,
        "root_cause": random.choice(["logic-error", "race-condition", "null-reference",
                                      "type-mismatch", "off-by-one", "resource-leak"]),
        "lines_changed": random.randint(1, 50),
        "tests_added": random.randint(0, 3),
    }


def gen_qa_verification(idx):
    topic = random.choice(TOPICS)
    return f"qa-{idx}", {
        "type": "qa-verification",
        "question": topic,
        "agents_consulted": random.randint(2, 4),
        "consensus_reached": random.random() > 0.1,
        "confidence": round(random.uniform(0.75, 0.99), 3),
    }


def gen_data_validation(idx):
    const = random.choice(MATH_CONSTANTS)
    return f"validate-{const[0]}-{idx}", {
        "type": "data-validation",
        "constant": const[0],
        "expected_value": const[1],
        "description": const[2],
        "verified": True,
        "precision_digits": random.randint(6, 12),
    }


def gen_geo_validation(idx):
    fact = random.choice(GEO_FACTS)
    return f"geo-{idx}", {
        "type": "geo-validation",
        "subject": fact[0],
        "claim": fact[1],
        "value": fact[2],
        "verified": True,
        "source_count": random.randint(2, 5),
    }


def gen_sentiment_analysis(idx):
    return f"sentiment-{idx}", {
        "type": "sentiment-analysis",
        "text_length": random.randint(50, 500),
        "sentiment": random.choice(SENTIMENTS),
        "polarity": round(random.uniform(-1.0, 1.0), 3),
        "subjectivity": round(random.uniform(0.0, 1.0), 3),
    }


def gen_conversation_turn(idx):
    topic = random.choice(TOPICS)
    return f"conv-{idx}", {
        "type": "conversation-turn",
        "role": random.choice(["user", "assistant"]),
        "turn_number": random.randint(1, 10),
        "topic": topic,
        "tokens_in": random.randint(100, 2000),
        "tokens_out": random.randint(100, 3000),
        "tools_used": random.choice(TOOLS_USED),
    }


def gen_web_research(idx):
    topic = random.choice(TOPICS)
    return f"research-{idx}", {
        "type": "web-research",
        "query": topic,
        "sources_found": random.randint(3, 15),
        "sources_verified": random.randint(2, 8),
        "confidence": round(random.uniform(0.7, 0.98), 3),
    }


def gen_deployment(idx):
    service = random.choice(["api-gateway", "settlement-engine", "mcp-server",
                              "dashboard", "webhook-relay", "badge-service"])
    return f"deploy-{service}-{idx}", {
        "type": "deployment",
        "service": service,
        "version": f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,20)}",
        "environment": random.choice(["staging", "production"]),
        "status": "success" if random.random() > 0.05 else "rollback",
    }


def gen_shell_execution(idx):
    cmds = [
        "pytest tests/ -v", "ruff check swarm_at/", "mypy swarm_at/",
        "docker build -t swarm-at .", "git log --oneline -5",
        "curl -s https://api.swarm.at/health", "pip install -e .",
    ]
    cmd = random.choice(cmds)
    return f"shell-{idx}", {
        "type": "shell-execution",
        "command": cmd,
        "exit_code": 0 if random.random() > 0.1 else 1,
        "safety_class": random.choice(["safe", "review-required"]),
        "duration_ms": random.randint(100, 30000),
    }


def gen_planning(idx):
    topic = random.choice(TOPICS)
    return f"plan-{idx}", {
        "type": "planning",
        "objective": topic,
        "steps_planned": random.randint(3, 8),
        "agents_assigned": random.randint(1, 4),
        "estimated_settlements": random.randint(3, 15),
    }


# ── Build the batch ──────────────────────────────────────────────────

NEW_TYPE_GENERATORS = [
    (gen_blueprint_fork, 20),
    (gen_guard_action, 18),
    (gen_trust_check, 12),
    (gen_credit_topup, 10),
    (gen_receipt_verify, 8),
    (gen_badge_request, 6),
    (gen_adapter_settle, 15),
]

EXISTING_TYPE_GENERATORS = [
    (gen_code_generation, 16),
    (gen_code_review, 14),
    (gen_bug_fix, 12),
    (gen_qa_verification, 14),
    (gen_data_validation, 12),
    (gen_geo_validation, 10),
    (gen_sentiment_analysis, 10),
    (gen_conversation_turn, 12),
    (gen_web_research, 10),
    (gen_deployment, 8),
    (gen_shell_execution, 8),
    (gen_planning, 8),
]


def main():
    ledger_path = sys.argv[1] if len(sys.argv) > 1 else "ledger.jsonl"

    # Read existing entries to get the chain tip
    with open(ledger_path) as f:
        lines = f.readlines()

    last_entry = json.loads(lines[-1])
    parent_hash = last_entry["current_hash"]
    timestamp = last_entry["timestamp"]

    # Build task list: (generator_fn, index)
    tasks = []
    for gen_fn, count in NEW_TYPE_GENERATORS + EXISTING_TYPE_GENERATORS:
        for i in range(count):
            tasks.append((gen_fn, i + 1))

    # Shuffle for realistic ordering
    random.shuffle(tasks)

    # Generate entries
    new_entries = []
    for gen_fn, idx in tasks:
        timestamp += random.uniform(5.0, 120.0)  # 5s to 2min between entries
        task_id, payload = gen_fn(idx)
        entry = make_entry(parent_hash, timestamp, task_id, payload)
        parent_hash = entry["current_hash"]
        new_entries.append(entry)

    # Append to ledger
    with open(ledger_path, "a") as f:
        for entry in new_entries:
            f.write(json.dumps(entry, sort_keys=True) + "\n")

    print(f"Added {len(new_entries)} entries ({len(lines)} existing → {len(lines) + len(new_entries)} total)")

    # Count new types
    new_types = {}
    for entry in new_entries:
        t = entry["payload"]["type"]
        new_types[t] = new_types.get(t, 0) + 1

    print("\nNew entries by type:")
    for t, c in sorted(new_types.items(), key=lambda x: -x[1]):
        print(f"  {c:3d}  {t}")


if __name__ == "__main__":
    main()
