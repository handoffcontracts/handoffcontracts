#!/usr/bin/env python3
"""
build_contract.py — turn a before/after draft pair (+ optional feedback) into a
hypothesis handoff contract, validated against the v0.2 schema.

Modes:
  real     : calls an LLM (Anthropic) to run editorial-diff -> extract -> playback.
             Requires ANTHROPIC_API_KEY and `pip install anthropic`.
  dry-run  : skips the LLM. Uses work/extract.json (produced upstream, e.g. by Claude
             in a Cowork session), then validates and assembles outputs. Lets you test
             the plumbing and the *reading* with no API setup.

Input dir conventions (--in DIR):
  before.(md|txt|docx|pdf)     early / rough draft        (needed for the diff)
  after.(md|txt|docx|pdf)      shipped / final version    (required)
  feedback.(md|txt|docx|pdf)   review comments/transcript (optional)

Outputs (outputs/): contract.yaml, provenance.json, playback.md
See "../PRD - exemplar-to-contract tool (working draft).md" for the design.
"""
from __future__ import annotations
import argparse, glob, json, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPTS, WORK, OUT = ROOT / "prompts", ROOT / "work", ROOT / "outputs"
VALIDATE = ROOT / "scripts" / "validate.py"


def read_artifact(path: Path) -> str:
    suf = path.suffix.lower()
    if suf in (".md", ".txt"):
        return path.read_text(encoding="utf-8")
    if suf == ".docx":
        try:
            import docx
        except ImportError:
            sys.exit(f"{path.name}: pip install python-docx to read .docx")
        return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)
    if suf == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            sys.exit(f"{path.name}: pip install pypdf to read .pdf")
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(path)).pages)
    sys.exit(f"{path.name}: unsupported format {suf}")


def find_one(indir: Path, stem: str) -> Path | None:
    hits = sorted(glob.glob(str(indir / f"{stem}.*")))
    return Path(hits[0]) if hits else None


def load_inputs(indir: Path) -> dict:
    out = {}
    for stem in ("before", "after", "feedback"):
        p = find_one(indir, stem)
        if p:
            out[stem] = read_artifact(p)
    if "after" not in out:
        sys.exit(f"{indir}: need at least an 'after.*' artifact")
    return out


def call_model(prompt: str, model: str) -> str:
    try:
        import anthropic
    except ImportError:
        sys.exit("real mode needs `pip install anthropic`, or use --dry-run")
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model, max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def fill(template: str, **kw) -> str:
    for k, v in kw.items():
        template = template.replace("{{" + k + "}}", v or "(none provided)")
    return template


def extract_json(text: str) -> dict:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1]
        t = t[4:] if t.startswith("json") else t
    return json.loads(t.strip())


def run_pipeline(inputs: dict, model: str) -> dict:
    diff = extract_json(call_model(fill(
        (PROMPTS / "01_editorial_diff.md").read_text(),
        before=inputs.get("before"), after=inputs["after"], feedback=inputs.get("feedback")), model))
    (WORK / "diff.json").write_text(json.dumps(diff, indent=2))
    extract = extract_json(call_model(fill(
        (PROMPTS / "02_extract_contract.md").read_text(),
        before=inputs.get("before"), after=inputs["after"], feedback=inputs.get("feedback"),
        diff=json.dumps(diff, indent=2)), model))
    (WORK / "extract.json").write_text(json.dumps(extract, indent=2))
    return extract


def assemble_playback(extract: dict) -> str:
    out = ["# Playback — correct me where I'm wrong\n"]
    if extract.get("aha"):
        out.append("## What I noticed about how you work\n")
        out += [f"- {a}" for a in extract["aha"]] + [""]
    if extract.get("needs_elicitation"):
        out.append("## The few things I couldn't infer\n")
        for n in extract["needs_elicitation"]:
            out.append(f"- {n.get('question') if isinstance(n, dict) else n}")
        out.append("")
    if not extract.get("needs_elicitation"):
        out.append("_Nothing left I need to ask — this one's fully drafted._\n")
    out.append("_Full contract: outputs/contract.md (friendly) or contract.yaml (raw)._")
    return "\n".join(out)


def render_contract_md(c: dict) -> str:
    """A human-readable rendering of the contract — YAML is for machines, this is for people."""
    L = ["# Handoff contract\n"]
    p = c.get("project") or {}
    if p.get("name"):
        L.append(f"**{p['name']}**  ")
    if p.get("brief"):
        L.append(f"{p['brief']}\n")
    if p.get("quality_spectrum"):
        L.append(f"**Quality bar:** {p['quality_spectrum']} — {p.get('quality_notes', '')}\n")
    for ct in c.get("contributors", []):
        L.append(f"## {ct.get('role') or ct.get('id')}  ·  _{ct.get('kind')}_\n")
        if ct.get("contributes"):
            L.append(f"**I contribute** — {ct['contributes']}\n")
        if ct.get("requires"):
            L.append("**I require**")
            for r in ct["requires"]:
                tag = " *(blocking)*" if r.get("blocking") else ""
                L.append(f"- {r.get('input')}{tag}")
            L.append("")
        if ct.get("returns"):
            L.append(f"**I return** — {ct['returns']}\n")
        if ct.get("done_looks_like"):
            L.append(f"**Done looks like** — {ct['done_looks_like']}\n")
        eff = ct.get("effort") or {}
        if eff:
            note = f" — {eff['notes']}" if eff.get("notes") else ""
            L.append(f"**Effort** — {eff.get('focused_days', '?')} focused days over {eff.get('elapsed_days', '?')} elapsed{note}\n")
        iu = ct.get("intended_use") or {}
        if iu.get("enables"):
            L.append(f"**This is for** — {'; '.join(iu['enables'])}")
        if iu.get("audience_level"):
            L.append(f"**Audience** — {iu['audience_level']}")
        if iu.get("not_for"):
            L.append(f"**Not for** — {'; '.join(iu['not_for'])}")
        if iu:
            L.append("")
        ex = ct.get("exemplar") or {}
        if ex.get("ref"):
            L.append(f"**Exemplar** — `{ex['ref']}` ({ex.get('access', '')})")
            ann = ex.get("annotations") or {}
            if ann.get("deliberate"):
                L.append("\n_Deliberate choices_")
                L += [f"- {d}" for d in ann["deliberate"]]
            if ann.get("imposed"):
                L.append("\n_Imposed_")
                L += [f"- {d}" for d in ann["imposed"]]
            if ann.get("near_miss"):
                L.append(f"\n_Near miss_ — {ann['near_miss']}")
            L.append("")
    return "\n".join(L)


def validate(path: Path) -> int:
    r = subprocess.run([sys.executable, str(VALIDATE), str(path)], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="indir", help="input dir with before/after/feedback")
    ap.add_argument("--dry-run", action="store_true", help="skip the LLM; use work/extract.json")
    ap.add_argument("--model", default="claude-sonnet-5")
    args = ap.parse_args()
    WORK.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)

    if args.dry_run:
        ep = WORK / "extract.json"
        if not ep.exists():
            sys.exit("dry-run needs work/extract.json (produced upstream)")
        extract = json.loads(ep.read_text())
    else:
        if not args.indir:
            sys.exit("real mode needs --in DIR (or pass --dry-run)")
        extract = run_pipeline(load_inputs(Path(args.indir)), args.model)

    contract = extract.get("contract")
    if contract is None:
        sys.exit("extract.json has no 'contract' key")
    cpath = OUT / "contract.yaml"
    cpath.write_text(yaml.safe_dump(contract, sort_keys=False, allow_unicode=True))
    (OUT / "provenance.json").write_text(json.dumps(extract.get("provenance", []), indent=2))
    (OUT / "playback.md").write_text(assemble_playback(extract))
    (OUT / "contract.md").write_text(render_contract_md(contract))

    print(f"wrote outputs/contract.yaml, contract.md, provenance.json, playback.md\n")
    print("--- schema validation ---")
    rc = validate(cpath)
    print("\n--- playback ---\n")
    print((OUT / "playback.md").read_text())
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
