#!/usr/bin/env python3
"""Standalone ledger chain verifier. Zero dependencies, Python 3.8+."""

import hashlib
import json
import sys


GENESIS_HASH = "0" * 64


def verify(path="ledger.jsonl"):
    expected_parent = GENESIS_HASH
    count = 0

    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            entry = json.loads(line)
            count += 1

            # Check parent chain
            if entry["parent_hash"] != expected_parent:
                print(
                    f"FAIL line {lineno}: parent_hash mismatch\n"
                    f"  expected: {expected_parent}\n"
                    f"  got:      {entry['parent_hash']}"
                )
                return False

            # Recompute hash: set current_hash to "", serialize with sorted keys
            stored_hash = entry["current_hash"]
            entry["current_hash"] = ""
            computed = hashlib.sha256(
                json.dumps(entry, sort_keys=True).encode()
            ).hexdigest()

            if computed != stored_hash:
                print(
                    f"FAIL line {lineno}: hash mismatch for task {entry['task_id']}\n"
                    f"  expected: {computed}\n"
                    f"  got:      {stored_hash}"
                )
                return False

            expected_parent = stored_hash

    print(f"OK: {count} entries, chain intact")
    return True


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "ledger.jsonl"
    sys.exit(0 if verify(path) else 1)
