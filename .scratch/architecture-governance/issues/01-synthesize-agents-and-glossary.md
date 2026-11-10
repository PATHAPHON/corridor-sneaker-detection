# 01: Synthesize AGENTS.md and GLOSSARY.md from ADRs

**What to build:** Extract architectural stack, build/test commands, conventions, module boundaries, canonical domain terms, and system invariants from `docs/adr/` into `AGENTS.md` and `GLOSSARY.md`, then update the knowledge graph.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] Extract tech stack, build/test commands, and conventions into `AGENTS.md`.
- [x] Codify canonical terms, forbidden synonyms, and 6 system invariants into `GLOSSARY.md`.
- [x] Run `graphify update .` to synchronize knowledge graph.
