#!/usr/bin/env bash
# Install the repository's immutable c2j pin into PREFIX/bin.
set -euo pipefail
repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
prefix=${1:?Usage: scripts/install-c2j.sh PREFIX}
mkdir -p "$prefix/bin"
prefix=$(cd "$prefix" && pwd)
pin=$(cat "$repo_root/.c2j-version")
case "$pin" in
  source:*)
    revision=${pin#source:}
    if [[ ! $revision =~ ^[0-9a-f]{40}$ ]]; then
      echo 'Source pins require a full Git commit ID.' >&2
      exit 1
    fi
    scratch=$(mktemp -d)
    trap 'rm -rf "$scratch"' EXIT
    git -C "$scratch" init -q
    git -C "$scratch" remote add origin https://github.com/colony-2/c2j.git
    git -C "$scratch" fetch --quiet --depth=1 origin "$revision"
    git -C "$scratch" checkout --quiet --detach FETCH_HEAD
    test "$(git -C "$scratch" rev-parse HEAD)" = "$revision"
    (
      cd "$scratch"
      go version
      go build -mod=readonly -buildvcs=false \
        -ldflags "-X github.com/colony-2/c2j/internal/buildinfo.version=source-$revision -X github.com/colony-2/c2j/internal/buildinfo.commit=$revision" \
        -o "$prefix/bin/c2j" ./cmd/c2j
    )
    ;;
  *)
    npm install --global --prefix "$prefix" "@colony2/c2j@$pin"
    npm view "@colony2/c2j@$pin" gitHead
    ;;
esac
"$prefix/bin/c2j" version
