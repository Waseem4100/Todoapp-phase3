<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- List of modified principles: Article IV (Technology Constraints) completely revised to reflect Phase I and Phase II requirements
- Added sections: Phase I and Phase II technology matrices, Phase Isolation Rules
- Removed sections: Generic technology constraints from previous version
- Templates requiring updates:
  - .specify/templates/spec-template.md (UP-TO-DATE)
  - .specify/templates/plan-template.md (UP-TO-DATE)
  - .specify/templates/tasks-template.md (UP-TO-DATE)
- Follow-up TODOs: None
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

### Phase I: In-Memory Console Application
* **Architecture**: Console application only
* **Storage**: In-memory only (no persistent storage)
* **Frontend**: None
* **Backend**: Simple command-line interface
* **Authentication**: Not allowed
* **Database**: Not allowed

### Phase II: Full-Stack Web Application
* **Backend**: Python REST API
* **Database**: Neon Serverless PostgreSQL
* **ORM/Data layer**: SQLModel or equivalent
* **Frontend**: Next.js (React, TypeScript)
* **Authentication**: Better Auth (signup/signin)
* **Architecture**: Full-stack web application
* **AI/Agent frameworks**: Not allowed until later phases

### AI & Orchestration (Phases III and Later)
* **OpenAI Agents SDK**
* **Model Context Protocol (MCP)**
* **Other AI/agent frameworks**: Only allowed starting Phase III

### Infrastructure (Later Phases Only, When Specified)
* **Docker**
* **Kubernetes**
* **Kafka**
* **Dapr**

### Phase Isolation Rules
* **Authentication**: Allowed starting Phase II only
* **Web frontend**: Allowed starting Phase II only
* **Neon PostgreSQL**: Allowed starting Phase II only
* **AI or agent frameworks**: Prohibited until Phase III and later
* No features, abstractions, or infrastructure from future phases may appear in earlier phases

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

**Version**: 1.1.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2026-02-03
