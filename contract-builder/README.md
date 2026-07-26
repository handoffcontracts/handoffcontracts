# contract-builder

The minimal-slice tool from the PRD: feed it a **before/after draft pair** (plus any reviewer feedback), and it drafts a **hypothesis handoff contract** — validated against the v0.2 schema — by reading the *transitions* between drafts, where tacit quality standards actually live.

This is the **logic core**, deliberately built first. The peripheral-panel / playback UI (Next.js) wraps this once the reading is trustworthy. See `../PRD - exemplar-to-contract tool (working draft).md`.

## How it works

1. **Editorial diff** (`prompts/01`) — reads before → after (+ feedback) and surfaces what was cut, tightened, reordered, or kept, and whether each change was deliberate or imposed.
2. **Extract** (`prompts/02`) — maps that reading onto the schema, filling only what the evidence supports. Never fabricates: gaps become targeted questions, not plausible guesses.
3. **Playback** (`prompts/03`) — reads the draft back, leading with what it noticed about how you work, then asks only the few non-obvious questions.

## Run it

Input dir holds `after.(md|txt|docx|pdf)` (required), plus `before.*` and `feedback.*` if you have them.

```bash
pip install -r requirements.txt

# real mode (needs ANTHROPIC_API_KEY)
python src/build_contract.py --in examples/my-substack-piece

# dry-run: no API. Uses work/extract.json produced upstream (e.g. by Claude in a
# Cowork session), then validates + assembles the outputs.
python src/build_contract.py --dry-run
```

Outputs land in `outputs/`: `contract.yaml`, `provenance.json`, `playback.md`.

## First test (Phase 4)

The fastest way to see whether the *reading* is any good, before wiring up an API key: drop a real before/after into `examples/`, have Claude produce `work/extract.json` from it in-session, then `--dry-run` to validate and see the playback. Log where its reading diverges from what you meant — and patch the PRD, not just the code.

## Status

v0, expect rough edges. Reuses the canonical schema (`schema/`) and validator (`scripts/validate.py`).
