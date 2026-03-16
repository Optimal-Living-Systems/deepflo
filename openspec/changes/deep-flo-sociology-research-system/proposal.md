# Proposal: Deep Flo Sociology Research System
**Change ID:** deep-flo-sociology-research-system
**Status:** Draft
**Created:** 2026-03-16
**Author:** Joel / OLS AI Lab
**OpenSpec Version:** 1.2.0

## What We Are Building

A fully autonomous, multi-stage sociology research pipeline built on Deep Flo + Deep Agents. Takes a topic as input. Outputs academic reports, accessible summaries, media-ready content, and OVNN-scored analysis. All stages run as Deep Agents sub-agents orchestrated by a director agent.

## The Seven Pipeline Stages

1. Topic Scoping & Question Formation
2. Literature Discovery (OpenAlex + Semantic Scholar + web)
3. Source Extraction & Methodology Evaluation
4. Thematic Synthesis (parallel SDT / political economy / community organizing lenses)
5. Academic Report Generation
6. Accessible Translation (plain language + social media + infographic briefs)
7. Review, Fact-Check & OVNN Scoring

## Why We Are Building It

- Core infrastructure for OLS Open Science Research Lab
- Produces sociology training data for CommunityLLM and OVNN
- Makes academic sociology accessible to mutual aid communities
- Demonstrates Deep Flo's value as an agentic research orchestrator

## Success Criteria

- [ ] Director agent accepts a topic and produces a research plan without human intervention
- [ ] Literature agent finds 10+ relevant sources via OpenAlex
- [ ] Extraction agent produces structured JSON per source
- [ ] Synthesis produces distinct analysis across at least 2 theoretical lenses
- [ ] Academic report is structurally valid
- [ ] Accessible summary requires no sociology background to understand
- [ ] OVNN scores generated for policy-relevant findings
- [ ] All outputs written to filesystem and ingested to LanceDB

## Scope

**In scope:** 7-stage pipeline, all Deep Agents skills/sub-agents, MCP tool connections (OpenAlex, LanceDB), Kestra scheduling, output schema

**Out of scope:** Frontend UI, fine-tuned Qwen model integration (Phase 2), HBoK personalization (Phase 3)
