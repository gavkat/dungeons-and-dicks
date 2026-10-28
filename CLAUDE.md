# CLAUDE.md

This repo is an [Obsidian](https://obsidian.md) vault, not a code project. It chronicles two D&D campaigns set in the same world on the Sword Coast:

- **Campaign 1: Lost Mine of Phandelver.** The Wolfpack's story. It is finished.
- **Campaign 2: Echoes of Phandelver.** The Boner Bros' story, set five years later. It is ongoing, and new sessions are added here.

Every note is a Markdown page. Notes link to each other with Obsidian `[[wikilinks]]`. The vault is also published as a website (see [Publishing](#publishing)).

## Folder structure

```
README.md                 Front page: session tables and an index of every entity (markdown links)
CLAUDE.md                 This file (left out of the website)
Shared/                   Notes that appear in BOTH campaigns (one page each, linked from both)
Campaign 1/
  Lost Mine of Phandelver.md    Campaign 1 hub
  Sessions/  Party/  NPCs/  Places/  Factions/  Items/  Lore/
Campaign 2/
  Echoes of Phandelver.md       Campaign 2 hub
  Open Threads.md               Active quests, mysteries, debts & enemies
  Sessions/  Party/  NPCs/  Places/  Factions/  Items/  Lore/
.claude/skills/           Repo skills (dnd-session-update and its check scripts)
.github/                  Website publishing workflow and scripts
.obsidian/                Obsidian app settings and plugins
_config.yml               Old Jekyll config. Nothing uses it now.
```

Only `README.md` and `CLAUDE.md` go at the repo root. Never add notes there. Each campaign folder has the same subfolders, and a note goes in the one that matches its first `**Tags:**` type:

| Subfolder | What goes in it | Tag |
|---|---|---|
| `Sessions/` | One page per session (see naming below) | `#session` |
| `Party/` | Player characters. Campaign 2's also holds the party page `Boner Bros.md` | `#character #pc` |
| `NPCs/` | Non-player characters, including group pages for minor mobs (e.g. `Walter & Kyle`, `Krug Gladiators`) | `#character #npc` |
| `Places/` | Locations: towns, dungeons, regions, ships | `#Location` |
| `Factions/` | Factions, crews, organizations, authorities | `#Faction` |
| `Items/` | Magic items, weapons, gear | `#Item` |
| `Lore/` | Lore, mechanics, laws, gods and powers | `#Lore`, `#Deity` |

The campaign hub pages, and Campaign 2's `Open Threads.md`, sit at the top of their campaign folder.

Use `Shared/` only for something that really appears in both campaigns, such as Wild Fury, Glenn, Ilbryn Darksight, Mordenkainen/Prometheus, Dave, Halia, Agatha the Hag, the Wolfpack, the Dark Six, Tymora, Beshaba, the Ilefarn, Phandelver's Pact, Leilon, Phandelver and the Lionshield Coster. `Shared/` has no subfolders. When an entity from one campaign first turns up in the other, move its note into `Shared/` and add `#Shared #Campaign1 #Campaign2` to its tags. Don't create a second page for it.

### Naming

- **Campaign 2 sessions:** `Session N.md`, just the number (the title goes in the page heading, `# Session N: Title`).
- **Campaign 1 sessions:** `Session N - Title.md`, plus `Prologue.md`, `Prequel - The Wild Sheep's Chase.md` and `Epilogue.md`.
- **Other notes:** named for the entity, exactly as written in the notes (e.g. `The Tempest's Temptation.md`).

## Linking rules

- **Wikilinks find notes by name, not folder.** Obsidian looks up a link like `[[Koa]]` by the note's file name anywhere in the vault, or by a frontmatter `aliases:` entry (e.g. `[[Prometheus]]` → `Shared/Mordenkainen.md`). So moving a note between folders never breaks its links, but every file name must be unique across the whole vault.
- **Name clashes:** give the newer file a qualifier, e.g. `The White Claw (Champion).md` next to the place `The White Claw.md`. Add a `> Not to be confused with [[The White Claw]]` line (pointing at the other note) to both notes, and link with an alias: `[[The White Claw (Champion)|The White Claw]]`.
- **Only `README.md` uses markdown links**, with the folder path written out and URL-encoded (`%20` for spaces, `%28`/`%29` for parentheses), e.g. `[Koa](Campaign%202/NPCs/Koa.md)`. If a note listed in the README moves, update its README link too.

## Workflow and tools

- **Adding a session:** use the `dnd-session-update` skill (`.claude/skills/dnd-session-update/SKILL.md`). It covers reading the recap, house style, page templates, which pages to update afterwards (campaign hub, README, `Boner Bros.md`, `Open Threads.md`), and the review pass.
- **Link check:** `python3 .claude/skills/dnd-session-update/scripts/check_links.py [--all]` (run from the repo root). By default it checks only changed files and reports broken wikilinks, broken README links and duplicate file names.
- **Coverage check:** `python3 .claude/skills/dnd-session-update/scripts/check_coverage.py N` or `--all`. It checks that every note a Campaign 2 session links to mentions that session, and that the hub and README list it. It reads sessions from `Campaign 2/Sessions/`.
- Run the link check after any edit, and both checks after a session update.

## Publishing

`.github/workflows/quartz.yml` builds the site with Quartz and deploys it to GitHub Pages on every push to `main`. `.github/scripts/prepare-quartz.sh` copies the vault into Quartz, leaving out the dot-folders, `CLAUDE.md`, `_config.yml` and canvases, and turns `README.md` into the homepage. `fix-links-for-quartz.py` fixes links Quartz can't resolve (e.g. `Dew-Dew Bun` vs `Dew Dew Bun`). Folder names become part of the site's page addresses.

## Don't

- Don't commit `.obsidian/plugins/flowershow/data.json`. It holds an API token and is gitignored.
- Don't commit scratch output (extracted PDF text, rendered PNGs) into the vault.
- Don't invent facts. Every claim in a note should trace back to a session recap (see the skill's review phase).
