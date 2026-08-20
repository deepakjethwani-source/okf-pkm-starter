---
description: Answer a question against the wiki and render it as a visual artifact
argument-hint: <your question> [as slides | as a chart]
allowed-tools: Read, Write, Bash, Glob, Grep
---

Answer the question in $ARGUMENTS against the wiki, starting from `wiki/index.md`
and following [[wikilinks]]. Then render the result into `outputs/`:
- prose synthesis → a well-structured `.md`
- "slides" → Marp-format markdown (`---` separators, front matter)
- "chart"/"plot" → run matplotlib via Bash, save the PNG, embed it in a `.md`

Cite the wiki pages you used. Then propose whether this output should be filed back
into `wiki/` as a new page. If I say yes:
- file it with OKF frontmatter (`type: Concept`, `generated`, and `sources`
  entries for the wiki pages it draws on), update `index.md`, and — if it shifts
  the thesis — `overview.md`;
- append a `**Query**` entry to `wiki/log.md` following the Logging convention in
  CLAUDE.md, noting the page it produced.
