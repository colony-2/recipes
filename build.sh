#!/usr/bin/env bash
# Narrow, read-only purpose-document checks; native recipe suites remain separate.
set -euo pipefail
export LC_ALL=C

fail() { printf 'Purpose check failed: %s\n' "$*" >&2; exit 1; }

[[ -f PURPOSE.md && -r PURPOSE.md && -s PURPOSE.md ]] ||
  fail 'PURPOSE.md must be a readable, nonempty regular file'

# Check the current document structure without pinning its prose or digest.
awk '
  function finish() { if (section != "" && content) populated[section] = 1 }
  /^##[[:space:]]/ {
    finish()
    section = $0
    sub(/^##[[:space:]]+/, "", section)
    sub(/[[:space:]#]+$/, "", section)
    content = 0
    next
  }
  /^[[:space:]]*$/ { next }
  !/^#/ && /[[:alnum:]]/ { content = 1 }
  END {
    finish()
    n = split("Purpose|Owns|Does not own|Interfaces|Boundary examples|Changing responsibilities", required, "|")
    for (i = 1; i <= n; i++) {
      if (!populated[required[i]]) {
        printf "Purpose check failed: missing or empty section: %s\n", required[i] > "/dev/stderr"
        bad = 1
      }
    }
    exit bad
  }
' PURPOSE.md
printf 'PASS: readable purpose document and populated responsibility/interface/boundary sections\n'

for evidence in AGENTS.md README.md build.yaml \
  recipes/kernel/consultation.yaml recipes/develop/develop.yaml \
  recipe-tests/consultation-kernel.test.yaml; do
  [[ -f "$evidence" ]] || fail "missing evidence file: $evidence"
done
printf 'PASS: six supporting instruction, workflow, and test files exist\n'

# Extract ordinary inline and reference-definition Markdown destinations.
# Inline code and fenced examples are not filesystem references.
destinations=$(awk '
  /^[[:space:]]*```/ || /^[[:space:]]*~~~/ { fence = !fence; next }
  fence { next }
  {
    line = $0
    gsub(/`[^`]*`/, "", line)
    if (match(line, /^[[:space:]]*\[[^]]+\]:[[:space:]]*/)) {
      print substr(line, RLENGTH + 1)
      next
    }
    while (match(line, /\[[^]]*\]\([^)]*\)/)) {
      link = substr(line, RSTART, RLENGTH)
      sub(/^[^]]*\]\(/, "", link)
      sub(/\)$/, "", link)
      print link
      line = substr(line, RSTART + RLENGTH)
    }
  }
' PURPOSE.md)
while IFS= read -r destination; do
  # Ignore optional titles, preserving angle-bracket destinations with spaces.
  destination="${destination#"${destination%%[![:space:]]*}"}"
  if [[ "$destination" == \<* ]]; then
    destination="${destination#<}"
    destination="${destination%%>*}"
  else
    destination="${destination%%[[:space:]]*}"
  fi
  [[ -n "$destination" ]] || continue
  [[ "$destination" == \#* || "$destination" == //* ||
     "$destination" =~ ^[[:alpha:]][[:alnum:]+.-]*: ]] && continue
  destination="${destination%%#*}"
  [[ -e "$destination" ]] || fail "broken local Markdown link: $destination"
done <<< "$destinations"
printf 'PASS: local Markdown link destinations (external URLs, fragments, and inline code excluded)\n'
printf 'Purpose structural and evidence-path checks passed. Manual ownership review and native recipe runtime tests remain separate.\n'
