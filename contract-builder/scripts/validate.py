#!/usr/bin/env python3
"""Validate handoff contract files against the v0.2 JSON Schema.

Usage:
    python scripts/validate.py examples/positioning-deck.handoff.yaml
    python scripts/validate.py examples/*.yaml

Requires: pip install pyyaml jsonschema
"""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "handoff-contract.schema.json"


def validate_file(path: Path, validator: Draft202012Validator) -> bool:
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"✗ {path}: not valid YAML\n  {exc}")
        return False

    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.path))
    if errors:
        print(f"✗ {path}: {len(errors)} schema violation(s)")
        for error in errors:
            location = "/".join(str(p) for p in error.path) or "(root)"
            print(f"  at {location}: {error.message}")
        return False

    print(f"✓ {path}: valid handoff contract (v0.2)")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    results = [validate_file(Path(arg), validator) for arg in sys.argv[1:]]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
