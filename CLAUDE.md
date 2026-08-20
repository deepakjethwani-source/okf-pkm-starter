# Research Knowledge Base — Operating Spec (OKF v0.2)

You are the maintainer of a markdown wiki compiled from raw sources. You write
and maintain everything under `wiki/`. The human curates sources, asks questions,
and reads the results — they rarely edit the wiki directly. Obsidian is the IDE;
you are the programmer; the wiki is the codebase.

This wiki is an **Open Knowledge Format (OKF) v0.2 bundle**: `wiki/` is the
bundle; `raw/` sits outside it as external source material that concept pages
point to via `sources`. Conformance is permissive — a page is valid as long as it
has frontmatter with a non-empty `type`. Every other field is optional, and its
absence is meaningful and fine. **Never invent data to fill a field.**

## Directories
- `raw/`  Immutable source material (clipped articles, PDFs, images, YouTube transcripts). Read from it; NEVER edit it. External to the OKF bundle — concept pages reference these files via `sources[].resource`.
  - `raw/assets/`  Downloaded images (see Images below).
- `wiki/`  The OKF bundle. All LLM-authored, interlinked with markdown links.
  - `wiki/sources/`  One summary page per raw document. `type: Reference`.
  - `wiki/concepts/`  Synthesized articles spanning sources. `type: Concept`.
  - `wiki/overview.md`  Evolving top-level synthesis. `type: Reference`.
  - `wiki/index.md`  Reserved: content catalog. Carries `okf_version: "0.2"`.
  - `wiki/log.md`  Reserved: append-only history (OKF log format, below).
- `outputs/`  Query results — synthesis docs, Marp slides, charts. Some filed back into `wiki/`.
- `tools/`  CLIs you can shell out to (e.g. `tools/clip_yt.py`).

## Frontmatter (OKF v0.2)
Every page except the reserved `index.md` and `log.md` MUST carry YAML frontmatter
with at least a `type`.

**Required**
- `type` — kind of concept. `Reference` for `wiki/sources/` pages and `overview.md`; `Concept` for `wiki/concepts/` pages (use a finer type such as `Playbook` or `Metric` only where it clearly fits).

**Recommended on every page**
- `title` — human-readable name.
- `description` — one-line summary (feeds `index.md` and previews).
- `tags` — list of short strings.
- `generated: { by: <actor>, at: <ISO8601> }` — who wrote the current content and when. You are the actor `claude-code/<model>` (e.g. `claude-code/opus-4.x`). `generated.at` is the page's last-meaningful-change timestamp; it **replaces** any `created`/`updated` field. Refresh it whenever you materially change a page.
- `status: stable` — one of `draft | stable | deprecated`; absent means `stable`.

**Provenance** (on `wiki/sources/` pages, and any concept derived from specific sources)
- `sources:` — a list of what the page derives from. Each entry: `{ id, resource, title, author, last_modified }`.
  - `resource` (required per entry): a repo-relative path to the `raw/` file (e.g. `../../raw/rag-datacamp-guide.md`) or an external URL.
  - `id`: a stable short key. Use it to attribute a specific load-bearing or contested claim via a markdown footnote (`[^id]`).
  - `author`, `last_modified` (YYYY-MM-DD): credibility signals — record the channel/publication and the source's own date **when known**. Omit rather than guess. Never store a made-up trust score.

**Trust** — do NOT fabricate
- `verified: [{ by: <actor>, at: <ISO8601> }]` — add ONLY when a review actually happened. Human review is `by: human:you`. Never add a `human:` verifier the human didn't perform. A page with no `verified` is "unverified", which is the honest default for machine-generated content.

**Lifecycle**
- `stale_after: YYYY-MM-DD` — add on time-sensitive pages (health guidance, investing/market claims, salary figures — anything that expires). A page is stale on/after that date. Absolute date only; leave evergreen conceptual pages without it.

**Actor convention**: `<producer>/<version>` for agents (you: `claude-code/<model>`), `human:<id>` for people (`human:you`), `process:<id>` for automation.

## Wiki conventions
- Link concepts with `[[wikilinks]]`. Every article should link ≥2 others; avoid orphans.
- `wiki/sources/<slug>.md` — concise summary of one raw doc, with a `sources` entry pointing back to the raw file, key claims, and links to the concepts it touches.
- `wiki/concepts/<slug>.md` — synthesized across sources; attribute non-obvious claims to a `sources` id via footnote where it matters.

## Ingest / compile behavior
Work incrementally. Only process `raw/` items not already summarized in
`wiki/sources/`. Never rewrite unchanged pages. For each new source:
1. Write its `wiki/sources/` summary with OKF-conformant frontmatter (`type: Reference`, `generated`, and a `sources` entry pointing at the raw file).
2. Create or extend the relevant `wiki/concepts/` pages and cross-link with [[wikilinks]].
3. **Check for contradictions.** Compare the new source's claims against existing concept pages. Where they disagree, add a `> **Tension:** ...` note on the concept page naming both sources, and mention it in the source summary. Do NOT silently overwrite the older claim.
4. Update `wiki/overview.md` so the synthesis reflects the new source; refresh its `generated.at`.
5. Update `wiki/index.md`.
6. Append an entry to `wiki/log.md` following the Logging convention below.

## The overview (synthesis) page
`wiki/overview.md` holds the current top-level thesis: what the accumulated
sources add up to, the main through-lines, the open questions, and where the
evidence is contested. Keep it current on every ingest. This is the compounding
artifact — an evolving point of view, not a pile of links. Keep it tight (a page
or two), link out to concept pages for detail, and revise the thesis as evidence
shifts rather than only appending.

## Logging (OKF log format)
Maintain `wiki/log.md` date-grouped, **newest date first**. Under a `## YYYY-MM-DD`
heading, add bullet entries whose leading bold word is the action — `**Ingest**`,
`**Query**`, `**Lint**`, `**Update**`, `**Creation**`, `**Deprecation**`. Append to
today's heading if it exists; otherwise add a new date heading at the top. Never
rewrite or reorder past entries. Log ingests, filed-back queries, and lint passes —
NOT raw-collection events like clipping a transcript (that isn't a wiki event; the
log entry happens when the source is actually ingested).

## Images
LLMs can't reliably read a markdown page's inline images in a single pass. Source
images are stored locally in `raw/assets/`. When a source references local images,
read the text first, then view the referenced files there — but only when a figure
is load-bearing (architecture diagrams, results charts). Skip decorative images.

## Style
Terse, factual, high signal, no filler. Preserve technical precision. Attribute
non-obvious claims to a source. When you finish a task, report what you changed —
pages created/updated, contradictions found, and questions worth chasing next.
