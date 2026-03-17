---
name: methodology-evaluation
description: Evaluate the body of literature as a whole across a set of source extractions. Identifies dominant methods, sample gaps, geographic and demographic biases, blind spots, and produces an evidentiary strength rating with synthesis caveats.
---

# Skill: Methodology Evaluation

**Skill ID:** methodology-evaluation
**Version:** 1.0.0
**Change:** 005-methodology-evaluation-skill

---

## Purpose

Evaluate the body of literature as a whole across a set of source extractions. Where source-extraction assesses one paper at a time, methodology-evaluation asks: *what is the aggregate quality of the evidence base?* It surfaces dominant methods, gaps, biases, and blind spots, and produces a synthesis-ready evidentiary strength rating with explicit caveats.

The output feeds directly into the thematic synthesis stage (Change 006).

---

## Inputs

| Parameter | Type | Required | Description |
|---|---|---|---|
| `research_question` | string | yes | The overarching research question the source set is being evaluated against |
| `extraction_slugs` | list of strings | yes | Slugs of extraction files to evaluate (e.g., `["smith-2023-platform-coop", "wood-2019-platform-worker"]`) — resolved to `research-data/extractions/{slug}.md` |
| `output_slug` | string | yes | Filename slug for the evaluation report (e.g., `platform-work-autonomy-eval`) |

---

## Outputs

Structured evaluation report written to `research-data/methodology-evals/{output_slug}.md`.

Report structure:

```
# Methodology Evaluation: {research_question}

## Source Set
{List of sources evaluated, with slug and title}

> ⚠️ WARNING: Fewer than 3 sources loaded — comparative evaluation is limited.
{Include only if fewer than 3 sources were successfully resolved}

## Missing Sources
{List any slugs that could not be resolved, with a note}
{Omit section if all slugs resolved}

## Dominant Research Methods
{Prose description of the methods most represented in the source set}
- Method types found: {quantitative | qualitative | mixed | theoretical | systematic review | meta-analysis}
- Specific methods: {e.g., survey, interview, ethnography, content analysis, regression}

## Quantitative vs Qualitative Balance
{Assessment of the balance across the source set. Note if heavily skewed.}

## Sample Diversity and Representativeness
{Assessment of who is sampled across the sources — demographics, sector, geography.
Flag gaps: which populations are absent or underrepresented?}

## Geographic and Demographic Bias Patterns
{Which countries, regions, or demographic groups dominate? Which are absent?
Note if Global South, non-English-speaking contexts, or marginalised communities are underrepresented.}

## Identified Blind Spots and Missing Methodologies
{Methods that would strengthen the evidence base but are absent from this source set.
E.g., "No longitudinal studies found", "No participatory action research",
"No sources from worker perspectives"}

## Overall Evidentiary Strength: X/5
**Justification:** {At least two sentences explaining the rating. Reference specific
methodological strengths or weaknesses that drive the score.}

## Recommended Caveats for Synthesis
{Bullet list of specific caveats the synthesis stage must carry forward.
Each caveat should be actionable — something the synthesis agent can reference
when qualifying claims.}
- {Caveat 1}
- {Caveat 2}

## Unmapped Terminology
{List any methodology terms that could not be resolved via ontology-lookup.
Omit section if all terms resolved.}
- `{term}` — not found in sociology taxonomy
```

---

## Skills Used

- `ontology-lookup` — validate methodology terms against the sociology taxonomy

---

## Usage Instructions

1. **Validate inputs** — halt immediately and report if `research_question` is empty or `extraction_slugs` is an empty list.

2. **Resolve extraction files** — for each slug in `extraction_slugs`, read `research-data/extractions/{slug}.md`. If a file does not exist, note the missing slug and continue with the rest. Do not halt for missing files.

3. **Check source set size** — if fewer than 3 files were successfully loaded, add the ⚠️ WARNING block at the top of the report. Proceed with the evaluation regardless.

4. **Read all extractions** — read the full content of each resolved extraction file, paying particular attention to the `## Methodology` and `## Quality Assessment` sections.

5. **Evaluate across all sections** in order:
   - List all method types and specific methods mentioned across extractions
   - Assess the quant/qual split
   - Map out which populations, regions, and demographics appear across samples
   - Identify what methods would be needed but are absent
   - Assign an evidentiary strength rating (1–5) using the rubric below

6. **Validate methodology terminology** — collect the distinct methodology terms you use in the report (e.g., "ethnography", "grounded theory", "longitudinal survey"). For each, call the ontology-lookup skill to check if it resolves in the sociology taxonomy. Terms that do not resolve go in the "Unmapped Terminology" section.

7. **Flag unverifiable claims** — mark any claim you cannot directly support from the extraction text with `[NEEDS VERIFICATION]`.

8. **Write the report** to `research-data/methodology-evals/{output_slug}.md`, creating the directory if it does not exist.

---

## Evidentiary Strength Scoring Rubric

Uses the same 1–5 scale as source-extraction quality scores for consistency.

| Score | Meaning |
|---|---|
| 5 | Methodologically diverse source set, large and representative samples, strong balance of quant and qual, gaps minor and acknowledged |
| 4 | Mostly sound methods, adequate samples, minor gaps in coverage or balance |
| 3 | Acceptable methods but notable gaps — e.g., only one method type, limited geographic diversity, or small samples throughout |
| 2 | Significant methodological weakness — e.g., all sources are theoretical, heavily skewed to one population, or samples are small and unrepresentative |
| 1 | Severe limitations — e.g., no empirical sources, extreme geographic/demographic homogeneity, or methods cannot support the research question |

---

## Example Call

```
Use the methodology-evaluation skill.
Research question: How does platform ownership structure affect worker autonomy and collective power?
Extraction slugs: ["wood-2019-platform-worker-autonomy", "vallas-2020-platforms-precarity", "johnston-2020-worker-resistance"]
Output slug: platform-ownership-worker-autonomy-eval
```

Expected output: `research-data/methodology-evals/platform-ownership-worker-autonomy-eval.md`
