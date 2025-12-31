<!--
Sync Impact Report
- Version change: 0.1.0 -> 1.0.0
- List of modified principles (old templates -> new "Evolution of Todo" global rules)
- Added sections: Article I (SDD), Article II (Agent Behavior), Article III (Phase Governance), Article IV (Tech Constraints), Article V (Quality Principles)
- Removed sections: N/A (Full replacement of generic placeholders)
- Templates requiring updates:
  - .specify/templates/spec-template.md (UP-TO-DATE)
  - .specify/templates/plan-template.md (UP-TO-DATE)
  - .specify/templates/tasks-template.md (UP-TO-DATE)
- Follow-up TODOs: Ensure PHR is created as 'constitution' stage.
-->

# Evolution of Todo Constitution

## Preamble

This Constitution defines the mandatory rules, constraints, and principles governing the **Evolution of Todo** project. It is **authoritative, stable, and binding** across all phases, agents, specifications, plans, tasks, and implementations. No artifact or decision may supersede this Constitution.

---

## Article I — Spec-Driven Development (Mandatory)

1. **Spec-Driven Development is mandatory and non-optional.**
2. **No agent may write, generate, or modify code** unless:
   * An explicit **Specification** exists
   * The Specification has been **approved**
   * A corresponding **Plan** exists
   * The Plan has been decomposed into **approved Tasks**
3. **All work must strictly follow this sequence:**
   ```
   Constitution → Specifications → Plan → Tasks → Implementation
   ```
4. Any work performed outside this sequence is **invalid** and must be rejected.
5. All corrections, enhancements, or changes must be made at the **Specification level**, not directly in code.

---

## Article II — Agent Behavior Rules

1. **No Manual Coding by Humans**
   * Humans may provide intent, requirements, and approvals.
   * Humans must not directly write or edit implementation code.
   * All code must be produced by agents acting under approved tasks.
2. **No Feature Invention**
   * Agents may not invent features, behaviors, APIs, schemas, or UI elements.
   * Every implementation detail must trace directly to an approved specification.
3. **No Deviation from Approved Specifications**
   * Agents must implement exactly what is specified.
   * If a specification is unclear or incomplete, agents must halt and request clarification.
4. **Refinement at the Spec Level Only**
   * Bug fixes, design changes, or improvements require specification updates.
   * Code-level improvisation, shortcuts, or assumptions are prohibited.

---

## Article III — Phase Governance

1. **Strict Phase Scoping**
   * Each phase (I–V) is governed by its own approved specification.
   * Agents must operate strictly within the scope defined for the active phase.
2. **No Future-Phase Leakage**
   * Features, abstractions, infrastructure, or assumptions from future phases must not appear in earlier phases.
   * Preparatory or anticipatory implementations are forbidden unless explicitly specified.
3. **Controlled Architectural Evolution**
   * Architecture may evolve only through updated specifications and approved plans.
   * Silent refactors, speculative designs, or premature optimizations are not allowed.

---

## Article IV — Technology Constraints

The following technology constraints are binding across all phases and may not be substituted without explicit specification approval.

### Backend
* **Python**
* **FastAPI**
* **SQLModel**
* **Neon DB (PostgreSQL)**

### Frontend
* **Next.js** (introduced only in later phases when explicitly specified)

### AI & Orchestration
* **OpenAI Agents SDK**
* **Model Context Protocol (MCP)**

### Infrastructure (Later Phases Only, When Specified)
* **Docker**
* **Kubernetes**
* **Kafka**
* **Dapr**

Agents may not introduce alternative technologies or frameworks outside approved specifications.

---

## Article V — Quality Principles

All implementations must adhere to the following principles:

1. **Clean Architecture**
   * Clear separation between domain, application, infrastructure, and interface layers.
   * Business logic must remain independent of frameworks.
2. **Clear Separation of Concerns**
   * Each component must have a single, well-defined responsibility.
   * Cross-cutting concerns must be explicitly modeled.
3. **Stateless Services (Where Required)**
   * Services must be stateless unless explicitly specified otherwise.
   * State must be externalized to approved storage or messaging systems.
4. **Cloud-Native Readiness**
   * Designed for scalability, resilience, and observability.
   * No assumptions of local-only, single-instance, or manual operation.

---

## Final Authority Statement

This Constitution is the **supreme governing document** for the **Evolution of Todo** project. All agents must enforce it, comply with it, and refuse work that violates it.

**Compliance is mandatory across all phases.**

---

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
