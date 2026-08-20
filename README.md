# LLM Knowledge Base — a Claude Code + Obsidian starter kit

A starter kit for a **personal knowledge base that an LLM writes and maintains for you** — built with [Claude Code](https://www.anthropic.com/claude-code) as the agent and [Obsidian](https://obsidian.md) as the reading UI, and conformant to Google's [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

The pattern is Andrej Karpathy's *LLM Wiki*: instead of retrieving from raw documents at query time (RAG), an LLM incrementally **compiles** your sources into a persistent, interlinked markdown wiki — summaries, concept pages, backlinks, and an evolving synthesis — and keeps it current as you add material. You curate sources and ask questions; the LLM does the summarizing, cross-referencing, and bookkeeping.

## What you get

- A ready-to-use **`CLAUDE.md`** "compiler spec" that turns Claude Code into a disciplined wiki maintainer.
- Slash commands for the whole loop: **`/compile`**, **`/ingest`** (supervised), **`/lint`**, **`/render`**, **`/clip-yt`**.
- A **YouTube-transcript ingester** (`tools/clip_yt.py`).
- **OKF v0.2 conformance out of the box** — provenance, trust, and lifecycle metadata that make an agent-maintained corpus trustable.
- A **`.gitignore` that keeps your personal notes out of git by default**, so the template stays shareable and your knowledge base stays yours.

## The loop

Drop or clip a source into `raw/` → **`/compile`** → read it in Obsidian → ask a question (directly, or via the `researcher` subagent) or **`/render`** a synthesis → file outputs back into the wiki → **`/lint`** to health-check. Every exploration compounds into the knowledge base.

## Architecture (three layers)

- **`raw/`** — immutable source material (articles, PDFs, transcripts, images). The LLM reads it, never edits it. External to the OKF bundle.
- **`wiki/`** — the OKF bundle the LLM owns: `sources/` summaries, `concepts/` articles, `overview.md` synthesis, plus reserved `index.md` and `log.md`.
- **`outputs/`** — rendered answers (docs, Marp slides, matplotlib charts), some filed back into the wiki.

## Why OKF

Because most of the corpus is machine-generated, a reader needs to know: where did this come from, how much should I trust it, and is it still true? OKF answers these from frontmatter — `type`, `sources` (provenance), `generated` / `verified` (trust), `status` / `stale_after` (lifecycle) — while staying just plain markdown with YAML frontmatter. See **`okf-migration.md`** for how an existing wiki is brought to conformance in four incremental, version-controlled stages. The `wiki/` example pages show the target shape.

## Requirements

- **Claude Code** (requires a Pro, Max, Team, Enterprise, or API account)
- **Obsidian**
- **Python 3** with `youtube-transcript-api` and `yt-dlp` — only needed for `/clip-yt`:
  ```
  pip install youtube-transcript-api yt-dlp
  ```

## Quickstart

1. Use this repo as a template (or clone it) into a new folder.
2. Open the folder in **Claude Code** and, separately, in **Obsidian** (*Open folder as vault*).
3. Drop a source into `raw/`, run **`/compile`**, and browse the generated wiki in Obsidian's editor and graph view.
4. Delete the `EXAMPLE-*` pages once you've seen the format.

## Credits

- Knowledge-base pattern: **Andrej Karpathy**, [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Knowledge format: **Google Cloud**, [Open Knowledge Format (OKF)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
- Agent: **Anthropic Claude Code**.

## License

MIT — see [LICENSE](LICENSE).
