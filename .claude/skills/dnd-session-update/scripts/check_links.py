#!/usr/bin/env python3
"""Validate the vault's cross-references. Run from the vault root.

Obsidian resolves [[wikilinks]] by note *basename* across the whole vault, so a
link is only broken if no .md file anywhere has that basename. The README also uses
URL-encoded markdown links whose decoded path must exist on disk. And two files
sharing a basename in different folders make [[links]] resolve unpredictably.

Usage:
    python check_links.py [file1.md file2.md ...]   # check only these files
    python check_links.py --all                      # check every .md in the vault
    python check_links.py                            # default: check git-changed .md files

Exit code is non-zero if any broken links are found, so it can gate a commit.
"""
import glob
import os
import re
import subprocess
import sys
import urllib.parse

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MDLINK = re.compile(r"\]\(([^)]+)\)")


def all_md():
    return glob.glob("**/*.md", recursive=True)


def frontmatter_aliases(path):
    """Obsidian resolves [[Name]] to a note's basename OR any of its YAML
    frontmatter `aliases`. Parse those (inline `[A, B]` or block `- A` form)
    without a yaml dependency so the checker matches Obsidian's real behavior."""
    try:
        with open(path) as fh:
            text = fh.read()
    except OSError:
        return set()
    if not text.startswith("---"):
        return set()
    end = text.find("\n---", 3)
    if end == -1:
        return set()
    fm = text[3:end]
    aliases = set()
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"\s*(aliases?|alias)\s*:\s*(.*)", line)
        if not m:
            continue
        rest = m.group(2).strip()
        if rest.startswith("["):  # inline list: aliases: [A, B]
            for a in rest.strip("[]").split(","):
                a = a.strip().strip("'\"")
                if a:
                    aliases.add(a)
        elif rest:  # single scalar: aliases: A
            aliases.add(rest.strip("'\""))
        else:  # block list on following indented "- " lines
            for follow in lines[i + 1:]:
                bm = re.match(r"\s*-\s*(.+)", follow)
                if not bm:
                    break
                aliases.add(bm.group(1).strip().strip("'\""))
    return aliases


def resolvable_names(paths):
    names = set()
    for p in paths:
        names.add(os.path.splitext(os.path.basename(p))[0])
        names |= frontmatter_aliases(p)
    return names


def changed_md():
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        ).stdout
    except Exception:
        return []
    files = []
    for line in out.splitlines():
        path = line[3:].strip().strip('"')
        if "->" in path:  # renames
            path = path.split("->")[-1].strip().strip('"')
        if path.endswith(".md") and os.path.exists(path):
            files.append(path)
    return files


def main():
    args = sys.argv[1:]
    note_basenames = resolvable_names(all_md())

    # Ambiguity check is always vault-wide.
    paths_by_base = {}
    for p in all_md():
        paths_by_base.setdefault(os.path.splitext(os.path.basename(p))[0], []).append(p)
    ambiguous = {b: ps for b, ps in paths_by_base.items() if len(ps) > 1}

    if args == ["--all"]:
        targets = all_md()
    elif args:
        targets = args
    else:
        targets = changed_md()
        if not targets:
            print("No changed .md files (pass filenames or --all to force a scan).")

    broken_wiki, broken_md = [], []
    for f in targets:
        text = open(f).read()
        for m in WIKILINK.finditer(text):
            # Inside Obsidian tables the alias pipe is escaped ("[[Target\|Display]]"),
            # so a trailing backslash is part of the escape, not the note name.
            target = m.group(1).strip().rstrip("\\").strip()
            if target == "wikilinks":  # the literal example in README.md
                continue
            if target not in note_basenames:
                broken_wiki.append((f, target))
        # README-style markdown links to local files
        for m in MDLINK.finditer(text):
            url = m.group(1)
            if url.startswith("http") or url.startswith("#"):
                continue
            path = urllib.parse.unquote(url.split("#")[0])
            if not os.path.exists(path):
                broken_md.append((f, url))

    ok = True
    if broken_wiki:
        ok = False
        print("BROKEN WIKILINKS:")
        for f, t in broken_wiki:
            print(f"  {f}: [[{t}]]")
    if broken_md:
        ok = False
        print("BROKEN MARKDOWN LINKS:")
        for f, u in broken_md:
            print(f"  {f}: ({u})")
    if ambiguous:
        print("AMBIGUOUS BASENAMES (same name in >1 folder — [[links]] are unpredictable):")
        for b, ps in ambiguous.items():
            print(f"  {b}: {ps}")

    if ok:
        print(f"All wikilinks and markdown links in {len(targets)} file(s) resolve OK.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
