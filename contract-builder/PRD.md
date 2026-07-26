# PRD — contract-builder (v0.2)

*A tool that drafts a handoff contract from a practitioner's own artifacts. Written using a human-centered PRD method, as a live test of that method. July 2026.*

**One line.** Feed it a before/after draft pair (plus any feedback), and it drafts a hypothesis handoff contract — validated against the [v0.2 schema](https://github.com/handoffcontracts/handoffcontracts/blob/main/handoff-contract.schema.json) — by reading the *transitions* between drafts, where tacit quality standards actually live.

**Scope of the minimal slice.** Artifacts in → a hypothesis contract mapped against the schema → one playback-and-correction pass. Not in this slice: the full elicitation probe loop, genre/variety clustering, the multi-party negotiation flow.

## 1. Ontological core

**Persona.** First user is the practitioner themselves, dogfooding against their own work (essays, decks, research reports). Eventual user: any senior practitioner with a corpus of past work and exacting, mostly-tacit standards.

**Problem.** Experienced practitioners carry exacting but mostly-tacit standards. The existing ways to make them explicit — forms, templates, briefs — impose blank-page and state-the-obvious overhead that the practitioner resents enough to skip. So the standards stay in the head and don't travel.

**Job-to-be-done.**

- *Functional* — turn artifacts I already have into a usable handoff contract, without a blank page or restating what's obvious from the work.
- *Emotional* — feel understood, not interrogated; relief that something already gets my bar, with zero sense of process overhead.
- *Social / introspective* — hand someone a legible version of my standards so I'm not misread, and confirm my own tacit bar is real and nameable.

## 2. Context and environmental state

**Empathy notes.** *Says* "I don't have time for more process." *Thinks* "you should be able to figure most of this out from my work." *Feels* burdened by prep, mildly insulted by obvious questions, relieved when something reflects them accurately. *Does* skips the form, relies on hallway calibration, re-explains "done" ad hoc every time.

**Emotional starting state.** Allergic to process overhead. Value must arrive *before* effort is demanded — the drop must return something felt-as-useful in the first minute, or the tool has already failed the job.

**Environment.** Artifacts are digital, scattered, and lifecycle-staged — living across documents, notebooks, AI chat threads, decks, and video. Rarely a single tidy file.

## 3. Interaction choreography — intake and pre-analysis

**Two artifact classes.** *Deliverables* are the polished outputs — the quality exemplars (what "good" looks like). *Surrogates* are the messy glue that deliverable taxonomies exclude — the process-and-rule anchors (how the work actually gets made, what gets checked).

**Surrogates are a process trace.** Read in sequence they form a lifecycle — capture, organize, synthesize, outline, draft, review, refine, compress. The tacit quality knowledge lives in the *transitions*, not in any single artifact. Diffing an early draft against the final is the cheapest route to the two hardest fields to elicit — a rejected near-miss, and which choices were deliberate versus imposed.

**Evidential-role weighting.** Weight artifacts by how truthful they are about real process: private working traces (a diary, draft diffs) are high-truth; audience-facing surrogates (a shared task list) are lower-truth and partly performance. Some surrogates are themselves claims.

**Minimal-slice intake.** Ingest a before/after draft pair plus any feedback artifact, and diff them. **Graceful degradation:** the diff is an accelerator, not a prerequisite. Evidence is a spectrum — more artifacts mean fewer questions; given only a polished exemplar, the tool still returns a sparser contract and asks only the non-obvious questions.

**Then:** assemble the hypothesis contract, map it to the schema, validate, and run one playback-and-correction pass that leads with what it noticed and asks only what it genuinely could not infer. Each answer fills a field and drops off the open-questions list.

## 4. Technical bounding box

**Reuse (fixed dependencies).** The v0.2 JSON Schema and its validator — the contract must validate.

**Pipeline.** (1) Ingest text-extractable formats. (2) Editorial diff — an LLM-driven semantic read of before → after (+ feedback): what was cut, tightened, reordered, kept, and whether deliberate or imposed. (3) Extract — map onto the schema, filling only what the evidence supports; never fabricate. (4) Validate. (5) Playback and one correction pass. (6) Output — the contract as raw YAML *and* a human-readable Markdown rendering, a provenance log, and the "aha" surfacing.

**Effort notation.** A simple, repeatable read on cost, added as a field: `focused_days` (concentrated work, fractions allowed) and `elapsed_days` (calendar span) — e.g. "2.5 focused days over 5 elapsed." Directly serves anyone scheduling handoffs around the contributor.

**Human-readable output.** YAML is machine plumbing; the tool also renders a friendly Markdown contract so a non-technical user can read it. A styled UI is a later wrapper, not part of this slice.

**Environment.** First build is the logic core in Python, reusing the existing validator — because the thing worth proving first is whether the *reading* is any good, which needs no UI. The peripheral-panel / playback interface (a small TypeScript app) wraps the core once the reading earns trust.

**Out of scope (this slice).** No full probe loop; no genre/variety clustering; no multi-party negotiation flow; no voice; no accounts or persistence; limited file formats.

## 5. Success heuristics

Two bars, weighted equally.

- **Introspective _aha!_.** In a dogfood session the tool surfaces at least one tacit standard the author hadn't consciously articulated, or catches a claim-versus-artifact contradiction. Judged by the author: "that's a real insight about how I work."
- **Portable artifact.** It produces a schema-valid contract a naive receiver could act on — needing correction, not rewriting.
- **Stated tradeoff / guardrail.** When completeness and honesty conflict, never fabricate to look finished; an honest gap beats a plausible guess.
- **Feeling of success.** "It showed me it already understood how I work before it asked me anything."

## 6. Acceptance criteria and the feedback loop

- Given a before/after + feedback set, returns a schema-valid contract with evidence links on filled fields, including candidate near-miss and deliberate/imposed annotations from the diff.
- Playback leads with what it noticed and asks only the non-obvious questions; each answer fills a field and closes the question.
- Degrades: given only a polished exemplar, still returns a sparser valid contract.
- **Feedback loop:** run it on real before/after sets; log where the reading diverges from intent; patch the PRD and prompts, not just the code.

## Status

The logic core is built and has been run against a real before/after (a published essay and its June draft, with the editorial plan as feedback). It produced a schema-valid contract, surfaced non-trivial tacit standards, and demonstrated the correction loop — an answered question filled the effort field and dropped off the open list.

**Next:** wire real-mode API calls and a leaner before/after to stress-test the diff without an explicit feedback file; a v0.3 schema pass (staged handoffs as an array, a size/extent facet, and the effort field, currently held); and the TypeScript playback UI.
