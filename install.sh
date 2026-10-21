#!/usr/bin/env bash
# Install the Masterplan skill for Claude Code.
#   ./install.sh            installs for your user (~/.claude/skills/masterplan)
#   ./install.sh --project  installs into the current project (.claude/skills/masterplan)
# Run it from a clone of this repository. Re-running it updates an existing install.
set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "$src/SKILL.md" ]]; then
  echo "SKILL.md not found next to install.sh; run this from a clone of the masterplan repository." >&2
  exit 1
fi

if [[ "${1:-}" == "--project" ]]; then
  dest="$(pwd)/.claude/skills/masterplan"
else
  dest="${HOME}/.claude/skills/masterplan"
fi

if [[ "$src" == "$dest" ]]; then
  echo "Already installed at $dest (this clone is the install)."
  exit 0
fi

mkdir -p "$dest"
# Copy only what the skill needs at run time.
for item in SKILL.md CREDITS.md LICENSE references assets scripts; do
  rm -rf "${dest:?}/$item"
  cp -R "$src/$item" "$dest/"
done

command -v python3 >/dev/null || echo "Note: the helper scripts need Python 3.8 or newer." >&2
command -v git >/dev/null || echo "Note: the build steps need git." >&2

echo "Installed Masterplan to $dest"
echo "Start a new Claude Code session and type: /masterplan <your idea>"
