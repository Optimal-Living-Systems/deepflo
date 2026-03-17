## 1. Skill File

- [x] 1.1 Create `skills/methodology-evaluation/SKILL.md` following the same structure as `skills/source-extraction/SKILL.md`
- [x] 1.2 Define inputs table: `research_question`, `extraction_slugs` (list), `output_slug`
- [x] 1.3 Define output: `research-data/methodology-evals/{output_slug}.md`
- [x] 1.4 Write full output template with all required sections (dominant methods, quant/qual balance, sample diversity, geographic/demographic bias, blind spots, evidentiary strength, synthesis caveats, unmapped terminology)
- [x] 1.5 Write step-by-step usage instructions including slug resolution, small-source-set warning, ontology-lookup call, and [NEEDS VERIFICATION] annotation rules
- [x] 1.6 Add evidentiary strength scoring rubric (1–5) matching source-extraction quality scale
- [x] 1.7 Add example call with sample inputs and expected output path

## 2. Agent References

- [x] 2.1 Update `AGENTS.md` (root) to add methodology-evaluation skill to the skills reference section
- [x] 2.2 Update `memories/AGENTS.md` (runtime) with the same methodology-evaluation entry

## 3. Output Directory Scaffold

- [x] 3.1 Create `research-data/methodology-evals/.gitkeep` so the output directory exists in the repo

## 4. OpenSpec Artifacts

- [x] 4.1 Verify proposal.md, design.md, specs/methodology-evaluation/spec.md, and tasks.md are all present and complete
- [ ] 4.2 Commit with message: `feat: add methodology-evaluation skill (OpenSpec 005)`
- [ ] 4.3 Push to remote
