## ADDED Requirements

### Requirement: Accept research question and source slugs as inputs
The skill SHALL accept a `research_question` string, a list of `extraction_slugs`, and an `output_slug` string as its inputs.

#### Scenario: Valid inputs provided
- **WHEN** the skill is called with a non-empty research question, at least one extraction slug, and an output slug
- **THEN** the skill proceeds to load and evaluate the extractions

#### Scenario: Missing research question
- **WHEN** the skill is called without a research question
- **THEN** the skill halts and reports the missing input before reading any files

#### Scenario: Empty extraction slug list
- **WHEN** the skill is called with an empty extraction_slugs list
- **THEN** the skill halts and reports that at least one extraction slug is required

---

### Requirement: Resolve extraction slugs to files
The skill SHALL resolve each extraction slug to `research-data/extractions/{slug}.md` and read the file contents.

#### Scenario: Extraction file exists
- **WHEN** a slug resolves to an existing file in research-data/extractions/
- **THEN** the skill reads the full file content for evaluation

#### Scenario: Extraction file missing
- **WHEN** a slug does not resolve to a file
- **THEN** the skill logs the missing slug and continues with the remaining extractions, noting the gap in the report

---

### Requirement: Warn when source set is small
The skill SHALL emit a visible warning in the report if fewer than 3 extraction files are successfully loaded.

#### Scenario: Fewer than 3 sources
- **WHEN** the resolved extraction set contains fewer than 3 files
- **THEN** the report opens with a warning that comparative evaluation is limited at this source count

---

### Requirement: Produce comparative methodology evaluation report
The skill SHALL produce a structured evaluation report covering: dominant research methods, quantitative vs qualitative balance, sample diversity and representativeness, geographic and demographic bias patterns, identified blind spots and missing methodologies, overall evidentiary strength rating (1–5) with justification, and recommended caveats for the synthesis stage.

#### Scenario: Full source set evaluated
- **WHEN** evaluation is complete over a source set of 3 or more extractions
- **THEN** the report contains all required sections with substantive content (not placeholder text)

#### Scenario: Evidentiary strength rating assigned
- **WHEN** the report is written
- **THEN** the evidentiary strength rating is a whole number from 1 to 5 accompanied by at least two sentences of explicit justification

---

### Requirement: Flag unverifiable claims
The skill SHALL mark any evaluation claim it cannot ground in the extraction text with `[NEEDS VERIFICATION]`.

#### Scenario: Claim cannot be confirmed from extraction text
- **WHEN** the agent makes an evaluation claim not directly supported by the loaded extractions
- **THEN** the claim is annotated inline with [NEEDS VERIFICATION]

---

### Requirement: Validate methodology terms via ontology-lookup
The skill SHALL call the ontology-lookup skill to check that methodology terms surfaced in the report are recognised in the sociology taxonomy. Unresolved terms SHALL be listed in an "Unmapped Terminology" section rather than blocking the evaluation.

#### Scenario: Term resolves in taxonomy
- **WHEN** a methodology term (e.g., "ethnography", "survey") is checked via ontology-lookup and found
- **THEN** the term is used as-is in the report

#### Scenario: Term does not resolve in taxonomy
- **WHEN** a methodology term is checked via ontology-lookup and not found
- **THEN** the term is still used in the report and added to the "Unmapped Terminology" section

---

### Requirement: Write output to standard path
The skill SHALL write the evaluation report to `research-data/methodology-evals/{output_slug}.md`, creating the directory if it does not exist.

#### Scenario: Output written successfully
- **WHEN** evaluation is complete
- **THEN** the file exists at research-data/methodology-evals/{output_slug}.md with all required sections populated

#### Scenario: Output directory does not exist
- **WHEN** research-data/methodology-evals/ does not yet exist
- **THEN** the skill creates the directory and writes the file without error
