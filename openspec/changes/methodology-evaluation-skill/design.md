## Context

Changes 001–004 established the research pipeline foundation: agent identity, literature search, per-source extraction, and the ontology layer. Source extraction (003) produces a structured `.md` file per source with a quality score and methodology fields. Synthesis (Change 006) will consume a set of sources and produce thematic analysis. The gap between extraction and synthesis is a cross-source methodology evaluation — a step that reads the full source set and asks whether the body of evidence is trustworthy, balanced, and sufficient to support the research question.

This skill is a document-in / document-out agent operation: it reads N extraction files, reasons over their collective methodology signals, and writes a single evaluation report.

## Goals / Non-Goals

**Goals:**
- Define a repeatable skill interface for comparative methodology evaluation
- Produce a structured report that synthesis agents can reference for caveats
- Validate methodology vocabulary against the sociology taxonomy via ontology-lookup
- Keep the skill stateless — no database, no external API calls beyond ontology-lookup

**Non-Goals:**
- Fetching or re-reading source documents (extractions are the authoritative input)
- Scoring individual sources (that is source-extraction's responsibility)
- Generating synthesis or recommendations (synthesis is Change 006)
- Automated test execution for this skill (skill testing is a later change)

## Decisions

**Decision 1 — Input as slugs, not file paths**
The skill accepts a list of extraction slugs (e.g., `smith-2023-platform-coop`) rather than raw file paths. The skill resolves them to `research-data/extractions/{slug}.md` internally.

*Why:* Slugs are stable identifiers shared across pipeline stages. File paths are implementation details that should not leak into skill interfaces.

*Alternative considered:* Accept full file paths directly. Rejected — couples callers to filesystem layout.

---

**Decision 2 — Output as a single Markdown report, not structured JSON**
The evaluation report is written as Markdown to `research-data/methodology-evals/{slug}.md`.

*Why:* Synthesis agents read Markdown natively (same pattern as extractions). A Markdown report is also human-readable without tooling, which matters for researcher review. Structured JSON would require a reader step before synthesis can use it.

*Alternative considered:* Dual output (Markdown + JSON sidecar). Deferred — unnecessary complexity for now; revisit at synthesis stage if the agent needs machine-parseable fields.

---

**Decision 3 — Ontology-lookup for terminology validation, not categorisation**
The skill calls ontology-lookup to check that methodology terms it surfaces (e.g., "ethnography", "survey", "content analysis") are recognised in the sociology taxonomy. It does NOT use ontology-lookup to auto-categorise sources.

*Why:* Categorisation requires judgment about a source's full content — that belongs in extraction. Terminology validation is a lightweight, deterministic check that keeps reports consistent with the controlled vocabulary.

---

**Decision 4 — Evidentiary strength uses the same 1–5 scale as source quality**
The overall evidentiary strength rating for the source set uses the same 1–5 rubric as source-extraction's per-source quality score, with explicit justification required.

*Why:* Consistent scale lets synthesis agents compare individual source quality against the aggregate body strength without conversion.

## Risks / Trade-offs

- **[Risk] Shallow extractions produce shallow evaluations** — If extraction files are incomplete or low-quality, the evaluation inherits those gaps. → Mitigation: the skill flags `[NEEDS VERIFICATION]` for any evaluation claim it cannot ground in the extraction text.

- **[Risk] Ontology vocabulary gaps** — Early taxonomy (Change 004) has limited L3/L4 coverage. Some methodology terms may not resolve. → Mitigation: unresolved terms are logged in the report under "Unmapped Terminology" rather than blocking evaluation.

- **[Risk] Source set too small** — An evaluation over 1–2 sources has limited comparative value. → Mitigation: the skill emits a warning in the report if fewer than 3 sources are provided.
