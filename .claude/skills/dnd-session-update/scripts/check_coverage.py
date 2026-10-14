#!/usr/bin/env python3
"""Find pages a session touched but never recorded. Run from the vault root.

Every entity a session page [[wikilinks]] should carry that session somewhere on
its own page (a `### Session N` history entry, or at least a `[[Session N]]`
citation). This reports each linked page that never mentions the session, plus
the hub pages that must list every session.

Usage:
    python check_coverage.py 19            # check Session 19 (Campaign 2)
    python check_coverage.py 17 18 19      # several sessions
    python check_coverage.py --all         # every Campaign 2 session (full audit)

Exit code is non-zero if anything is missing.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_links import frontmatter_aliases  # noqa: E402  (same resolution rules as the link checker)

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

# Pages that must mention every Campaign 2 session.
HUBS = ["Echoes of Phandelver.md", "README.md"]
# Pages that are only indexes, so a missing session there means nothing.
SKIP = {"README", "Open Threads", "Echoes of Phandelver", "Lost Mine of Phandelver"}


def index():
    """Map every name a [[link]] can resolve to — basename or frontmatter alias — to its file."""
    by_name, aliases = {}, {}
    for p in glob.glob("**/*.md", recursive=True):
        if p.startswith(".") or "/." in p:
            continue
        by_name.setdefault(os.path.splitext(os.path.basename(p))[0], p)
        for a in frontmatter_aliases(p):
            aliases.setdefault(a, p)
    for a, p in aliases.items():
        by_name.setdefault(a, p)  # a real basename wins over an alias
    return by_name


def mentions(text, n):
    # [[Session N]], [[Session N|...]], "### Session N", or README's Session%20N.md
    pat = rf"(\[\[Session {n}(\||\]\])|^#+\s*Session {n}\b|Session%20{n}\.md|\*\*\[\[Session {n}\]\]\*\*)"
    return re.search(pat, text, re.M) is not None


def check(n, by_name):
    path = f"Sessions/Session {n}.md"
    if not os.path.exists(path):
        print(f"Session {n}: no {path}")
        return 1
    text = open(path).read()
    targets = sorted({m.group(1).strip() for m in WIKILINK.finditer(text)})
    missing = []
    for t in targets:
        if t in SKIP or re.fullmatch(r"Session \d+", t):
            continue
        p = by_name.get(t)
        if p is None:
            missing.append(f"  [[{t}]] has no page (run check_links.py)")
        elif not mentions(open(p).read(), n):
            missing.append(f"  {p}  - linked from Session {n} but never mentions it")
    for h in HUBS:
        if not mentions(open(h).read(), n):
            missing.append(f"  {h}  - hub does not list Session {n}")
    if missing:
        print(f"Session {n}: {len(missing)} page(s) not updated")
        print("\n".join(missing))
        return 1
    print(f"Session {n}: all {len(targets)} linked pages and hubs record it")
    return 0


def main(argv):
    by_name = index()
    if argv == ["--all"]:
        nums = sorted(int(m.group(1)) for p in glob.glob("Sessions/Session *.md")
                      if (m := re.search(r"Session (\d+)\.md$", p)))
    else:
        nums = [int(a) for a in argv]
    if not nums:
        print(__doc__)
        return 2
    return 1 if sum(check(n, by_name) for n in nums) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
