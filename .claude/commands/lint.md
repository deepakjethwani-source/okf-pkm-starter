---
description: Health-check the wiki for integrity issues
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
---

Audit the wiki:
1. Broken or orphaned [[wikilinks]]; pages with no inbound links.
2. Contradictory or duplicated claims across pages (cross-check existing `> **Tension:**` notes).
3. Stale claims — flag any page whose `stale_after` date has passed, plus claims newer sources have superseded.
4. OKF conformance: every non-reserved page has frontmatter with a `type`; `wiki/index.md` carries `okf_version`.
5. Concepts mentioned repeatedly but lacking their own page.
6. Data gaps you could fill with a web search (flag before writing anything).
7. Candidate connections for new concept pages, and questions worth investigating.

Fix mechanical issues directly (broken links, index drift, missing back-links,
missing `type`). Propose judgment calls rather than acting on them. Write the full
report to `outputs/lint-<today's date>.md`.

Finally, append a `**Lint**` entry to `wiki/log.md` following the Logging
convention in CLAUDE.md, with a 1–3 bullet summary of what you found and fixed.
