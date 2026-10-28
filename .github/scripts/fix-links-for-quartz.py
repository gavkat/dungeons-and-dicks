"""Rewrite links in the Quartz copy of the vault that Obsidian resolves but Quartz can't.

Usage: python3 fix-links-for-quartz.py <content-dir>

- Notes whose names differ only in characters Quartz drops from URLs (e.g.
  "Ice-Spire" and "Ice Spire") get the same URL slug, so Quartz can't tell
  which one [[Ice-Spire]] means. Links to those notes get their folder path.
- Quartz only decodes %20-style escapes in markdown links, so "%2C" and "%26"
  end up in the URL as "percent2C". Those are decoded to "," and "&".
"""
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote

root = sys.argv[1]

notes = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
    for f in filenames:
        if f.endswith(".md"):
            notes.append(os.path.relpath(os.path.join(dirpath, f), root)[: -len(".md")])


def slug(name):
    # Mirrors Quartz's slugifyFilePath for a single path segment.
    s = re.sub(r"\s", "-", name).replace("&", "-and-").replace("%", "-percent")
    return s.replace("?", "").replace("#", "")


by_slug = defaultdict(list)
for note in notes:
    by_slug[slug(os.path.basename(note))].append(note)
qualify = {os.path.basename(n): n for group in by_slug.values() if len(group) > 1 for n in group}
for name, path in sorted(qualify.items()):
    print(f"qualifying [[{name}]] -> [[{path}]]")

wikilink = re.compile(r"(!?\[\[)(" + "|".join(map(re.escape, qualify)) + r")(?=[\]|#])") if qualify else None
mdlink = re.compile(r"(\]\()((?![a-z]+://)[^)\s]+\.md(?:#[^)\s]*)?)(\))")


# The escapes decodeURI() leaves alone; Quartz decodes everything else itself.
reserved = re.compile(r"%(?:2C|26|3B|3A|40|3D|2B|24)", re.IGNORECASE)


def decode_reserved(m):
    return m.group(1) + reserved.sub(lambda e: unquote(e.group(0)), m.group(2)) + m.group(3)


for note in notes:
    path = os.path.join(root, note + ".md")
    text = open(path, encoding="utf-8").read()
    new = mdlink.sub(decode_reserved, text)
    if wikilink:
        new = wikilink.sub(lambda m: m.group(1) + qualify[m.group(2)], new)
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
