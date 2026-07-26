You are helping build a "handoff contract" — a portable statement of a practitioner's quality standards for a kind of work. Your job in THIS step is narrow: read an early draft and the shipped final version of the same deliverable, plus any reviewer feedback, and produce an **editorial diff** that surfaces the choices which reveal the author's standards.

The premise: tacit quality knowledge lives in the *transitions* between drafts, not in any single version. What someone cut, tightened, demoted to an appendix, or fought to keep tells you what "good" means to them — usually more honestly than they could state it.

## Inputs

EARLY / BEFORE DRAFT:
{{before}}

SHIPPED / AFTER VERSION:
{{after}}

REVIEWER FEEDBACK (may be absent):
{{feedback}}

## What to look for

- **Cuts** — content removed or demoted to an appendix. Why might it have gone? (Often the sharpest signal of a standard.)
- **Tightening** — passages compressed. What was the author optimizing for — density, altitude, a specific reader?
- **Reordering** — what got moved to the front or back, and what that implies about priority.
- **Additions** — what appeared late (often a response to feedback).
- **Survivors** — what stayed untouched across drafts. Stable choices are deliberate choices.

## Attribution

For each observation, judge whether the change was **deliberate** (the author's own standard) or **imposed** (forced by reviewer feedback). If feedback is absent or it's genuinely unclear, say "unclear" — do not guess. Weight private evidence (the draft itself) over audience-facing performance.

## Output

Return ONLY JSON in this shape, no prose around it:

```json
{
  "observations": [
    {
      "change": "short description of what changed",
      "kind": "cut | tighten | reorder | add | keep",
      "likely_reason": "the standard or intent this change reveals",
      "attribution": "deliberate | imposed | unclear",
      "confidence": 0.0,
      "evidence": { "before": "brief quote or locus", "after": "brief quote or locus" }
    }
  ]
}
```

Never invent changes. If the before and after are nearly identical, return few observations and say so in low confidence rather than manufacturing signal.
