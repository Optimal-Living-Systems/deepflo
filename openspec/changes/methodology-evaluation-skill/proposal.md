## Why

Source extraction (Change 003) produces per-source quality scores, but nothing evaluates the body of literature as a whole — what methods dominate, what's missing, and whether the evidence base is strong enough to support synthesis. Without this, the synthesis stage operates blind to systematic bias or evidentiary gaps.

## What Changes

- New skill `methodology-evaluation` added to `skills/methodology-evaluation/SKILL.md`
- Skill reads a set of source extractions and produces a comparative methodology evaluation report
- Evaluation written to `research-data/methodology-evals/{slug}.md`
- Ontology-lookup skill called to validate methodology terms against the sociology taxonomy
- AGENTS.md updated to reference the new skill

## Capabilities

### New Capabilities

- `methodology-evaluation`: Comparative methodology evaluation across a set of extracted sources — identifies dominant methods, sample gaps, geographic/demographic biases, missing methodologies, and produces an overall evidentiary strength rating with synthesis caveats.

### Modified Capabilities

<!-- None — no existing spec-level behavior changes -->

## Impact

- New file: `skills/methodology-evaluation/SKILL.md`
- New output path: `research-data/methodology-evals/` (created at runtime)
- Depends on: source-extraction outputs (`research-data/extractions/*.md`), ontology-lookup skill
- Updates: `AGENTS.md` (root), `memories/AGENTS.md` (runtime)
- No breaking changes to existing skills
