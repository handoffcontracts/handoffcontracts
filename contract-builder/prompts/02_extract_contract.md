You are drafting a **hypothesis handoff contract** for the author of a deliverable, from their artifacts and an editorial diff. The contract states, for one contributor and one genre of work, what they contribute, what they require, what they return, what "done" looks like, and what the work is for — anchored to this exemplar with annotations that capture the quality choices behind it.

This is a HYPOTHESIS to be corrected, not a finished contract. Your reader will fix it. So the cardinal rule:

**Never fabricate to look complete.** If the evidence doesn't support a field, leave it out of the contract and add it to `needs_elicitation` as a targeted question. An honest gap beats a plausible guess. This is the single most important instruction here.

## Inputs

AFTER / FINAL:
{{after}}

BEFORE / EARLY (may be absent):
{{before}}

REVIEWER FEEDBACK (may be absent):
{{feedback}}

EDITORIAL DIFF (from the prior step):
{{diff}}

## The schema (v0.2), condensed

A contract is `{ handoff_contract: "0.2", project?: {...}, contributors: [ contributor ] }`.

Fill a single `contributor` with `kind: "human"` and:
- `contributes` — what they produce (name it concretely).
- `requires` — inputs they need to begin (array of `{input, from?, blocking?}`).
- `returns` — the deliverable, named concretely and in language a *receiver* could match against their own `requires`.
- `done_looks_like` — acceptance criteria at the handoff, framed as "what the receiver did NOT have to ask."
- `intended_use` — `{ enables: [...], audience_level, not_for: [...] }`. `not_for` is high-value; infer it from what the work pointedly avoids.
- `exemplar` — `{ ref, access, provenance?: {setting, decision_enabled, audience}, annotations?: {deliberate: [...], imposed: [...], near_miss} }`.
- `delta` — only if a specific target project differs from the exemplar; otherwise omit.
- `handoff` — `{ to?, checkpoint: "advisory", reviewer? }` for a human contributor.

Optional `project` block: `{ name?, brief?, quality_spectrum?: "sketch|working|polished|production", quality_notes?, glossary? }`.

## Surrogate → field mapping (how to read the evidence)

- Editorial diff **cuts / survivors** → `annotations.deliberate` and `annotations.near_miss` (the near-miss is what the early draft did that the final rejected).
- Editorial diff changes attributed **imposed** → `annotations.imposed`.
- Final's structure and argument spine → `returns`, `done_looks_like`.
- Register, density, length relative to the exemplar → `delta.register`, `delta.fidelity`, or `quality_spectrum` — but express size as a comparison, never an absolute rule.
- Reviewer feedback → receiver expectations → `done_looks_like`, `intended_use.audience_level`.

## Output

Return ONLY JSON, no prose:

```json
{
  "contract": { "handoff_contract": "0.2", "contributors": [ { "id": "author", "kind": "human", "...": "..." } ] },
  "provenance": [ { "field": "contributors[0].done_looks_like", "source": "after / diff", "evidence": "brief locus", "confidence": 0.0 } ],
  "needs_elicitation": [ { "field": "contributors[0].requires", "question": "a targeted, NON-obvious question — never ask what the artifacts already answer" } ],
  "aha": [ "a standard the author likely holds tacitly but may not have articulated, or a place their own drafts contradict what they'd probably claim" ]
}
```

The `aha` list is the payoff: surface one or two genuine, non-trivial observations about how this person works — especially contradictions between what they'd likely say and what the drafts actually show.
