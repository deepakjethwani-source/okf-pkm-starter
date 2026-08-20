# OKF v0.2 Migration Playbook

Retrofitting the existing wiki to OKF v0.2, in four stages. Run them **one at a
time**, in order. After each: run `/lint`, eyeball the changes (`git status`,
`git diff`), then commit. Git makes every stage reversible — if a pass looks
wrong, `git restore .` and try again.

Prereq: drop in the new `CLAUDE.md` and command files first, and commit that as
its own step (`git commit -m "Adopt OKF v0.2 conventions in CLAUDE.md + commands"`)
so new pages are born OKF-shaped before you touch the old ones.

---

## Stage 1 — Conformance (add `type`)

Paste into Claude Code:

> OKF v0.2 Stage 1 — conformance. For every `.md` file under `wiki/` EXCEPT
> `index.md` and `log.md`: ensure YAML frontmatter exists and add a `type` field —
> `Reference` for pages in `wiki/sources/` and `wiki/overview.md`, `Concept` for
> pages in `wiki/concepts/` (use a finer type like `Playbook` or `Metric` only
> where it clearly fits). Preserve all existing frontmatter and body content. Also
> add `okf_version: "0.2"` to the frontmatter of `wiki/index.md` (the only index
> file permitted frontmatter). Add no other OKF fields yet. Report the files
> changed and the `type` you assigned each.

Then: `/lint` → review → `git add . && git commit -m "OKF Stage 1: type conformance"`

At this point you are OKF-conformant. Everything below is additive enrichment.

---

## Stage 2 — Provenance (`sources`)

> OKF v0.2 Stage 2 — provenance. For each page in `wiki/sources/`, add a `sources`
> frontmatter list. Each summarizes exactly one raw file, so add one entry:
> `{ id: <short-slug>, resource: <repo-relative path to the raw file, e.g.
> ../../raw/some-source.md>, title: <source title> }`. Where the raw file's
> frontmatter or content reveals the author/channel and publication date, also add
> `author:` and `last_modified:` (YYYY-MM-DD). If you can't determine one, omit it
> — do not guess. For the two RAG sources previously flagged as missing
> author/published metadata, use web search to fill them if you're confident;
> otherwise leave them omitted and list them. For concept pages that clearly derive
> from specific sources, you may add the same `sources` entries. Report what you
> added and what you left blank.

Then: `/lint` → review → `git add . && git commit -m "OKF Stage 2: provenance"`

---

## Stage 3 — Trust + Lifecycle (`generated`, `status`, `stale_after`)

> OKF v0.2 Stage 3 — trust and lifecycle. For every page in `wiki/` except
> `index.md`/`log.md`:
> 1. Add `generated: { by: claude-code/<your model id>, at: <ISO8601> }`. For `at`,
>    use the file's last commit date from git history if available, otherwise the
>    existing `created` date. Do not invent precise times — a date at T00:00:00Z is
>    fine.
> 2. Migrate any existing `created`/`updated` fields into `generated` and remove them.
> 3. Add `status: stable`.
> 4. Add `stale_after: YYYY-MM-DD` ONLY on time-sensitive pages — health guidance,
>    investing/market claims, career/salary figures that will age — choosing a
>    sensible horizon (e.g. ~12 months out). Leave evergreen conceptual pages
>    without it.
> Do NOT add any `verified` field — human review hasn't happened, and fabricating
> it would be dishonest. Report which pages you marked `stale_after` and why.

Then: `/lint` → review → `git add . && git commit -m "OKF Stage 3: trust + lifecycle"`

---

## Stage 4 — Log format + version

> OKF v0.2 Stage 4 — reformat `wiki/log.md` to OKF log format: `## YYYY-MM-DD`
> date headings, newest date first, with bullet entries whose leading bold word is
> the action (`**Ingest**`, `**Query**`, `**Lint**`). Preserve the information in
> existing entries; just reorganize into newest-first date groups. Do not fabricate
> entries for history that was never logged. Confirm `wiki/index.md` carries
> `okf_version: "0.2"` from Stage 1.

Then: review → `git add . && git commit -m "OKF Stage 4: log format + version"`

---

## Ongoing (not a stage): `verified`

`verified` is earned, not migrated. As you actually read and confirm a page, tell
Claude Code to add `verified: { by: human:you, at: <today ISO8601> }` to it.
Over time your "human-reviewed" tier grows to mark exactly the pages you trust —
the direct antidote to silent trust drift.
