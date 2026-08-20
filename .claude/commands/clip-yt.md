---
description: Fetch a YouTube transcript + metadata into raw/ as a Markdown file
argument-hint: <youtube-url> [--timestamps]
allowed-tools: Bash, Read, Glob
---

The user wants to clip a YouTube video into the knowledge base. Input: $ARGUMENTS

Do this:

1. Run the helper script, keeping the URL in quotes and passing through any extra
   flags the user included (e.g. `--timestamps`):

   `python tools/clip_yt.py "<URL from input>" --out raw`

   (On some systems the command is `python3` instead of `python` — if `python`
   isn't found, retry with `python3`.)

2. Read the file the script reports it saved, and confirm the YAML front matter
   (title, channel, url, video_id, upload_date, duration) is populated. If title
   and date are empty, note that yt-dlp may not be installed — the transcript is
   still fine, just lower on metadata.

3. Report back the saved path, the video title, and the transcript word count.
   If the script says captions are disabled or the transcript is empty, tell the
   user plainly rather than inventing content.

Never edit or "clean up" the transcript text yourself — it is raw source
material. The `/compile` step will summarize and integrate it into the wiki later.
