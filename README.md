# Handoff contracts

**A lightweight contract format for quality expectations at the handoffs between people and AI agents.**

AI has made drafting cheap and calibration scarce. The result is “workslop”: work that looks finished and quietly transfers its repair costs downstream. The damage concentrates at handoffs — the joints between contributors who lack the shared history to know what “good” means to each other.

A handoff contract makes those expectations explicit and portable — agreed up front, when a collaboration is being set up, rather than sprung at the moment work changes hands (and, for work a contributor offers repeatedly, pre-staged before the project begins). Each contributor — human or AI agent — declares five things:

- **What I contribute** — the deliverable, named concretely
- **What I require** — the inputs I need before starting
- **What I return** — the form the work arrives in
- **What “done” looks like** — acceptance criteria at my handoff point
- **What it’s for** — the decisions it enables, the audience it serves, and what it is *not* for

…anchored by an **exemplar** (“like the NewCo marketing report”) plus a **constrained delta** (“shorter; board audience, not product team”). Senior practitioners already talk this way. This project formalizes it.

A collaboration usually has several handoffs — schedule-setting, kickoff, the interim exchange of interdependent work, draft review, final delivery — and a contract names what “done” means at each, rather than leaving it to be discovered late.

## Status

🚧 **Early and unstable.** This is a research provocation with a v0.2 draft schema, not a finished standard. Expect breaking changes. The concept is described in depth at [handoffcontracts.com](https://handoffcontracts.com) and in writing at [The UX Humanist](https://uxhumanist.substack.com).

## A minimal example

```yaml
handoff_contract: "0.2"

contributor:
  id: strategist-jk
  kind: human
  contributes: "Positioning analysis and two recommendations"
  requires:
    - input: "Competitor feature matrix"
      from: agent-claude
      blocking: true
  returns: "Annotated outline, 12–15 slides' worth of argument"
  done_looks_like: "Designer can build slides without asking
                    what any bullet means"
  exemplar:
    ref: "exidx://jk/2024-samsung-positioning"
    access: redacted
  delta:
    scope: "5 competitors, not 9"
    audience: "Board, not product team"
```

Enforcement is deliberately asymmetric: AI agents **fail closed** on missing required inputs; humans get **advisory checkpoints** that flag divergence at handoff. Humans get norms; agents get schemas.

## Validating a contract

The schema is machine-enforceable. To check a contract file:

```bash
pip install pyyaml jsonschema
python scripts/validate.py examples/positioning-deck.handoff.yaml
```

The schema enforces the format’s design commitments: the delta
vocabulary is closed (unknown dimensions are rejected), and
`checkpoint` accepts only `advisory` or `fail_closed`. See
[`schema/handoff-contract.schema.json`](schema/handoff-contract.schema.json)
for the annotated field reference.

## What’s here (and coming)

| Item | Status |
|---|---|
| v0.2 schema, machine-validatable ([`schema/`](schema/)) | Draft |
| Worked example ([`examples/`](examples/)) | Draft |
| `HANDOFF.md` authoring convention | Draft |
| Federated context-file template (shared standards vs. individual judgment) | In progress — target Sept 2026 |
| Agent A/B experiment harness (same brief, with/without contract, blind-judged) | In progress — target Sept 2026 |
| Calibration interview protocol | In progress |

## Relationship to MCP (and a disambiguation)

Handoff contracts borrow a move that worked for machines: the [Model Context Protocol](https://modelcontextprotocol.io) standardized how AI tools declare what they require and provide. This project applies that contract discipline to the *human and hybrid* side of collaboration — quality expectations, not tool schemas. It is **not affiliated with** Anthropic’s MCP, nor with Innovaccer’s Healthcare Model Context Protocol (HMCP).

It also extends, rather than duplicates, two adjacent conversations: structural coordination for zero-history teams ([flash teams](https://hci.stanford.edu/publications/2012/flashteams/flashteams-uist2012.pdf)) and the economics of [AI task chaining](https://www.nber.org/papers/w34859), which finds that the cost of handing off intermediate outputs is central to where AI’s value lands.

## Get involved

This project is looking for collaborators who want to break it in instructive places: does the delta vocabulary survive contact with real practitioners? Can a synthetic exemplar preserve the quality signal of a confidential one? Open an issue, or reach out via [handoffcontracts.com](https://handoffcontracts.com).

## License

Code is [MIT](LICENSE)-licensed. Specification text and documentation are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share and adapt freely, with attribution.

© 2026 David McGaw
