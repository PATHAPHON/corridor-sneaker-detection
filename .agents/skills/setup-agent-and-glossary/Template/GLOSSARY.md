# Project Glossary & Domain Invariants (GLOSSARY.md Template)

> [!IMPORTANT]
> **Status: Draft (Pending ADR Setup)**
> This is a baseline draft. Establish your Architecture Decision Record under `docs/adr/` and invoke the `setup-agent-and-glossary` skill to define domain entities, processes, and invariants.

Single Source of Truth (SSOT) for domain terminology, architectural invariants, and naming standards across this project.

---

## 1. Domain Terminology

**[Primary Entity 1]**:
[Definition and purpose of the entity].
_Avoid_: [List forbidden synonyms or confusing terms]

**[Primary Entity 2]**:
[Definition and purpose of the entity].
_Avoid_: [List forbidden synonyms or confusing terms]

**[Process / Operation]**:
[Definition of the workflow or process].
_Avoid_: [List forbidden synonyms or confusing terms]

---

## 2. System Invariants & Non-Negotiable Rules

- **[Invariant 1 - e.g. Data Grounding]**:
  [Strict rule regarding where data comes from, e.g. "Only use data that exists in the database. Never fabricate mock fallbacks."]
- **[Invariant 2 - e.g. Idempotency / Determinism]**:
  [Strict rule regarding operations or pipeline reproducibility.]
- **[Invariant 3 - e.g. Resource Safety]**:
  [Strict rule regarding memory, GPU, disk, or network usage.]
