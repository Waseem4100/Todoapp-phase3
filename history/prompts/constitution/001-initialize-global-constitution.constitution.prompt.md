---
id: 1
title: "Initialize global project constitution"
stage: constitution
date: 2025-12-31
surface: "agent"
model: "claude-sonnet-4-5"
feature: "none"
branch: "master"
user: "human"
command: "/sp.constitution"
labels: ["constitution", "initialization", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  - "Manual validation of template placeholders"
---

## Prompt

Below is a **single, global constitution** for the **“Evolution of Todo”** project.
It is written to apply uniformly across **Phase I through Phase V** and to act as the **supreme governing document for all agents**.

---

# Evolution of Todo

## Global Project Constitution (Phase I–V)

### Preamble

This Constitution defines the mandatory rules, constraints, and principles governing the **Evolution of Todo** project.
It is **authoritative, stable, and binding** across all phases, agents, tructure, or assumptions from future phases must not appear in earlier phases.
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

* **Next.js** (introduced only inspecifications, plans, tasks, and implementations.

No artifact or decision may supersede this Constitution.

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

   * Features, abstractions, infras later phases when explicitly specified)

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

   * Clear separation between domain, application, infrastructure, and interface layers
   * Business logic must remain independent of frameworks

2. **Clear Separation of Concerns**

   * Each component must have a single, well-defined responsibility
   * Cross-cutting concerns must be explicitly modeled

3. **Stateless Services (Where Required)**

   * Services must be stateless unless explicitly specified otherwise
   * State must be externalized to approved storage or messaging systems

4. **Cloud-Native Readiness**

   * Designed for scalability, resilience, and observability
   * No assumptions of local-only, single-instance, or manual operation

---

## Final Authority Statement

This Constitution is the **supreme governing document** for the **Evolution of Todo** project.
All agents must enforce it, comply with it, and refuse work that violates it.

**Compliance is mandatory across all phases.**

## Response snapshot

Established the project constitution at .specify/memory/constitution.md based on the "Evolution of Todo" global document. Updated plan-template.md to include specific constitution compliance checks for Articles I-V. Validated that all work now follows the mandatory Constitution → Spec → Plan → Tasks → Implementation sequence.

## Outcome

- ✅ Impact: High. Established the supreme governing document for the project.
- 🧪 Tests: Manual inspection of template consistency.
- 📁 Files: .specify/memory/constitution.md, .specify/templates/plan-template.md
- 🔁 Next prompts: Use /sp.specify to create the first feature specification.
- 🧠 Reflection: The transition from generic templates to a specific global constitution ensures strict governance across all phases of the "Evolution of Todo" project.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
