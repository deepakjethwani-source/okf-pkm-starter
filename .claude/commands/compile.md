---
description: Incrementally compile new raw/ sources into the wiki (batch, autonomous)
allowed-tools: Read, Write, Edit, Glob, Grep
---

Compile the wiki. Batch, run-and-review mode; to ingest a single source you want
to steer, use `/ingest` instead. Write all pages with OKF-conformant frontmatter
per the Frontmatter section of CLAUDE.md.

1. List everything in `raw/`. Compare against `wiki/sources/` to find sources not
   yet summarized.
2. For each new source, write `wiki/sources/<slug>.md` — a concise summary with
   OKF frontmatter: `type: Reference`, `generated: { by, at }`, and a `sources`
   entry whose `resource` points at the raw file (repo-relative). Add `author` /
   `last_modified` only if known; never guess.
3. Create or extend `wiki/concepts/<slug>.md` pages spanning sources, cross-linked
   with [[wikilinks]] and `type: Concept`.
4. Contradiction check: compare each new source against existing concept pages.
   Where they disagree, add a `> **Tension:** ...` note naming both sources, and
   mention it in the source summary. Never silently overwrite an older claim.
5. Update `wiki/overview.md` (refresh its `generated.at`) and `wiki/index.md`.
6. Append an entry to `wiki/log.md` following the Logging convention in CLAUDE.md.
7. Report: new sources, new/extended concepts, contradictions surfaced, and
   questions worth investigating next.
