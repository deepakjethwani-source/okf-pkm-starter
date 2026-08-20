---
description: Ingest ONE source with discussion before filing (supervised mode)
argument-hint: [path to a raw/ file — defaults to the newest unindexed one]
allowed-tools: Read, Write, Edit, Glob, Grep
---

Supervised, one-source-at-a-time ingest. Input: $ARGUMENTS. Follow the Frontmatter
and Logging conventions in CLAUDE.md.

1. Pick the source: if a path is given, use it; otherwise the newest file in `raw/`
   with no summary yet in `wiki/sources/`.
2. Read it in full. If it references load-bearing local images in `raw/assets/`,
   read the text first, then view those images.
3. STOP and discuss before writing anything. Present:
   - 3–6 key takeaways in your own words.
   - How it connects to existing wiki concepts (with [[links]]).
   - Any contradictions with what the wiki currently claims.
   - What you propose to create or update, plus 1–2 questions on what to emphasize.
   Then ask how I'd like to proceed. Do NOT write wiki pages yet.
4. After I respond, file it the way `/compile` does — OKF-conformant source summary
   (`type: Reference`, `generated`, `sources`), concept pages, `> **Tension:**`
   notes, `overview.md`, `index.md`, and a `wiki/log.md` entry — steered by my
   guidance.
