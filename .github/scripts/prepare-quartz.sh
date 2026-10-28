#!/usr/bin/env bash
# Copy the vault into a Quartz checkout and point Quartz's config at this site.
# Usage: prepare-quartz.sh <vault-dir> <quartz-dir> <base-url>
#   base-url has no protocol, e.g. gavkat.github.io/dungeons-and-dicks
set -euo pipefail

vault=$1
quartz=$2
base_url=$3

# Publish the notes only: no tooling, Obsidian settings, or the old Jekyll config.
# .git comes along so Quartz can read each note's last-modified date from history.
rm -rf "$quartz/content"
mkdir -p "$quartz/content"
tar -C "$vault" -cf - \
  --exclude './.github' --exclude './.claude' --exclude './.obsidian' \
  --exclude './.gitignore' --exclude './_config.yml' --exclude '*.canvas' \
  . | tar -C "$quartz/content" -xf -

# Quartz uses index.md as the homepage.
mv "$quartz/content/README.md" "$quartz/content/index.md"

python3 "$(dirname "$0")/fix-links-for-quartz.py" "$quartz/content"

cd "$quartz"

# Each edit is checked so a change upstream fails the build instead of
# silently publishing Quartz's defaults.
replace() {
  local file=$1 before
  before=$(cat "$file")
  perl -0pi -e "$2" "$file"
  [[ "$(cat "$file")" != "$before" ]] || { echo "no match in $file for: $2" >&2; exit 1; }
}

replace quartz.config.ts 's/pageTitle: "Quartz 4"/pageTitle: "Dungeons & Dicks"/'
replace quartz.config.ts "s|baseUrl: \"quartz.jzhao.xyz\"|baseUrl: \"$base_url\"|"
# No third-party analytics.
replace quartz.config.ts 's/analytics: \{\s*provider: "plausible",\s*\}/analytics: null/'
# Every note already opens with its own "# Title", so drop Quartz's duplicate heading on note pages
# (the first ArticleTitle in the file; folder and tag pages keep theirs).
replace quartz.layout.ts 's/(defaultContentPageLayout.*?)\n    Component\.ArticleTitle\(\),/$1/s'
# Inline #tags on notes two or more folders deep link outside the site: the tag URL
# is built as "../../tags/x" and Quartz's link resolver only expects "./"-prefixed
# paths. Given "/tags/x", it builds the right relative path at any depth.
replace quartz/plugins/transformers/ofm.ts 's|url: base \+ `/tags/\$\{tag\}`|url: `/tags/\$\{tag\}`|'
