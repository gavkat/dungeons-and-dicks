---
name: dnd-session-update
description: >-
  Ingest a session recap (a PDF, image, or pasted text of the latest D&D session)
  and update this Obsidian campaign vault end-to-end: create the new session page,
  create pages for any new NPCs/locations/factions/items/lore, update every entity
  the session touched, refresh the hub pages (README, campaign hub, Open Threads),
  then run a review pass that cross-checks every wikilink and every claim against
  the source. Use this whenever the user hands over a session summary/recap/writeup
  (in any format) and wants the vault brought up to date — including phrasings like
  "update all entities," "add the latest session," "create new pages where needed,"
  "update the vault from this PDF," or "make sure the links work and nothing was made
  up." Trigger even if they don't say the word "skill" or name the files explicitly.
---

# D&D Session → Vault Update

This vault (`Dungeons & Dicks`) chronicles two linked D&D campaigns in Obsidian markdown. Your job: take a recap of the newest session and fold it into the vault the way a careful archivist would — new session page, new entity pages, every affected page updated, hubs refreshed — then **prove your work** by validating links and checking every statement against the source. The whole value of this vault is that it's *trustworthy and cross-linked*: a broken link or an invented detail is worse than a missing one.

Work through the five phases below in order. Don't skip the review phase — it's the point.

---

## Phase 1 — Read the source (don't trust the text layer alone)

These recaps usually arrive as a **PDF that is one very tall page**: a title, a few paragraphs of prose, and character/scene illustrations. The harness may report a misleading page count. The prose lives in a text layer, but the **title and the artwork often carry real information that never appears in the text** — e.g. the session title, or art revealing a character's species. So always look at both.

- **Text + images in one pass:** run `scripts/extract_pdf.py <file.pdf>`. It writes the text layer to `<scratchpad>/session_text.txt` and renders each page to a PNG, and reports page count + how many embedded images each page has. If `pymupdf` isn't installed, it installs it (poppler/`pdftotext` is typically unavailable here — don't fight it, use the script).
- **Actually view the rendered PNG** with the Read tool. Read the title. Study the illustrations for details the prose omits.
- If the source is an image or pasted text instead of a PDF, just read it directly — same discipline about squeezing detail from any art.

Before moving on, write yourself a short plain-text list of **every concrete fact** the session establishes: who did what, who died, what was revealed, new names, new places, deaths, reveals. This list is your source of truth for Phase 5.

## Phase 2 — Learn the conventions before writing anything

The vault has a consistent house style. Match it exactly; a page that looks foreign is a tell that it was bolted on. Read these first:

- `README.md` — the navigation hub: campaign session tables and the full entity index (grouped: Antagonists, Allies, Places, Factions, Items…).
- The campaign hub for the campaign this session belongs to (`Echoes of Phandelver.md` for Campaign 2, `Campaign 1/Lost Mine of Phandelver.md` for Campaign 1) — has the session list, a "Story So Far" narrative, and a party/quest table.
- `Open Threads.md` — Active Quests, Mysteries, Debts & Enemies. This is where unresolved hooks live and get resolved.
- **The most recent existing session page** — copy its exact structure.
- One existing page of **each entity type you'll touch** (a PC, an NPC, a location, a faction, an item), to copy their structure.

### Where things live (folder → type)

| Folder | Contents |
|---|---|
| `Sessions/` | Campaign 2 sessions, named `Session N.md` (bare number) |
| `Campaign 1/Sessions/` | Campaign 1 sessions, named `Session N - Title.md` |
| `Party/`, `Campaign 1/Party/` | player characters (PCs) |
| `NPCs/`, `Campaign 1/NPCs/` | non-player characters |
| `Shared/` | people/places/powers that appear in **both** campaigns (one page, linked from both) |
| repo root (`./`) | most Campaign 2 locations, factions, items, and lore |

Which campaign does this session belong to? Check the recap's title/branding and the most recent session number. Put the new session and its new entities in that campaign's folders (Campaign 2 → `Sessions/`, `NPCs/`, root; use `Shared/` only if the entity genuinely spans both campaigns).

### Page templates (match these)

**Session page** (`Sessions/Session N.md`):
```markdown
# Session N: Title

**Tags:** #session

**In short:** one-sentence semicolon-separated teaser, richly [[wikilinked]].

## Summary

Prose, one paragraph per beat, [[wikilinking]] every entity on first mention in each paragraph.

## Key Developments

- **Bolded lead-in:** the consequential facts, each [[wikilinked]].
```

**NPC / location / faction / item / lore page:**
```markdown
# Name

**Tags:** #character #npc #Campaign2      ← use the tag set the sibling pages use for that type

## Description       ← "## Overview" for locations/factions/items/lore
Who/what they are.

## Role in Campaign
How they matter.

## Session History
### Session N
- what happened this session, [[wikilinked]].
```

**PC page** uses `### Character Concept` + `**Core Traits:**` bullets + a `## Session History` with `### Session N` subheads. Don't invent this structure — open the actual PC page and mirror it.

Tag sets vary by type (`#character #npc`, `#Location`, `#Faction`, `#Item`, `#Lore`) and campaign (`#Campaign2`). Copy whatever the sibling pages use rather than guessing.

## Phase 3 — Inventory, then create

From your Phase 1 fact list, enumerate every entity the session mentions. Then find out what already exists — search the whole vault, because an entity may live in a folder you didn't expect and may be referenced without its own page yet:

```
Grep each proper noun across *.md (output_mode files_with_matches).
```

Sort them into **create** vs **update**. Then:

1. **Write the session page** first (it anchors every `### Session N` bullet you'll add elsewhere).
2. **Create new entity pages.** Judgment calls:
   - **Minor one-off NPCs** (a knot of mooks introduced and mostly killed in one scene) read better as a **single combined page** — the vault already does this (e.g. `Walter & Kyle`, `The Dendrar Family`). Make one group page rather than four stubs.
   - **Name collisions matter** because Obsidian resolves `[[links]]` by *basename*. If a new entity shares a name with an existing page (e.g. an arena called "The White Claw" and a champion *also* called "The White Claw"), disambiguate the new file (`The White Claw (Champion).md`), add a `> Not to be confused with [[...]]` note to both, and link with a piped alias: `[[The White Claw (Champion)|The White Claw]]`.
   - Don't create a page for something the source only names in passing with nothing to say about it. A one-line mention can live inside the session page and the relevant entity's history instead.

## Phase 4 — Update everything the session touched

Ripple the session outward. For **each** affected existing page:

- Add a `### Session N` entry to its **Session History** with what it did/experienced.
- Update the **Description / Role / Core Traits** when the session *revealed* something durable (a new species, a true identity, a death, a resolved goal) — not just for a routine appearance.

Then the **hubs** (easy to forget, and the most visible):

- `README.md` — add the session to the campaign's session table; add any new entities to the appropriate lines of the entity index (using the URL-encoded markdown link format the file already uses, e.g. `[Name](NPCs/Name.md)` with `%20`/`%28`/`%29` encoding).
- **Campaign hub** — append the session to the session list, extend the "Story So Far" with the new beats, and update the party/quest table if a personal quest advanced or resolved.
- `Open Threads.md` — this is high-value. Move resolved hooks to a resolved state (the vault marks these inline, e.g. `**FOUND (Session N)**` or strikethrough), add new quests/mysteries the session opened, and update ones that advanced. A session that answers an old mystery *and* opens two new ones should show all three.

Keep the vault's voice: concise, wry, present-tense-ish narration, and cite the session in `([[Session N]])` form the way sibling text does.

## Phase 5 — Review: links, then fidelity (never skip)

This is what makes the update trustworthy. Two independent checks:

### 5a. Every link must resolve
Run `scripts/check_links.py` from the vault root. It scans the files you changed (or `--all`) and reports:
- **broken `[[wikilinks]]`** — a target with no matching note basename anywhere in the vault (ignore the literal `[[wikilinks]]` example in `README.md`);
- **broken README markdown links** — a URL-decoded path that doesn't exist on disk;
- **ambiguous basenames** — the same basename in two folders, which makes `[[links]]` resolve unpredictably.

By default it checks only the **git-changed** files (what your session touched) — that's the signal you care about. Fix everything it flags there and re-run until clean. (A new file with a parenthetical name must be linked with that exact basename — the most common self-inflicted break.) The checker honors Obsidian frontmatter `aliases:`, so a link like `[[Prometheus]]` resolves to the page that declares that alias (`Shared/Mordenkainen.md`) rather than reading as broken. `--all` audits the whole vault; if it flags something you didn't touch, it's pre-existing — don't fix longstanding issues unless asked.

### 5b. Every claim must trace to the source — nothing invented
Reread your Phase 1 fact list against everything you wrote. The vault's credibility depends on this. Specifically:
- **Don't add plot, motives, outcomes, names, or numbers the source doesn't state.** If the recap doesn't say a character survived, don't say they did.
- **Inferences are allowed but must be marked as such and stay minimal.** Genealogy (a Tabaxi's father is a Tabaxi), elimination ("human and warforged were refused" + a known-human party member ⇒ the other is the warforged), and art-based details (species visible in an illustration) are fair — but phrase them as implied/revealed and keep the certainty honest. Apply the same standard consistently: if you infer one character's species from their child, do it for the parallel case too.
- **When the source is ambiguous or clearly typo'd** (a name that contradicts established facts, an actor that doesn't parse), prefer the faithful, non-committal rendering (passive voice, the established spelling) over inventing a resolution — and surface the call to the user.

### Report back
Tell the user, concisely: what session was added, which pages were **created** vs **updated**, the result of the link check (e.g. "all N wikilinks resolve"), and any **judgment calls or inferences** you made in 5b so they can veto them. Transparency here is the deliverable as much as the edits are.

## Committing

Stage and commit with a clear message summarizing new vs updated pages. **Only push or open a PR if the user asks** — and follow any branch rules in the environment. Don't assume the session content and this bookkeeping belong in the same PR as unrelated work.
