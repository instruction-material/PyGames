#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$root"

fail() {
  printf 'course source verification failed: %s\n' "$1" >&2
  exit 1
}

require_file() {
  [ -f "$1" ] || fail "missing $1"
}

require_file "COURSE_SOURCE_MANIFEST.md"
require_file "SOURCE_BACKLOG.md"
require_file "Check-in-2-Starter.py"
require_file "Check-in-3-Starter.py"
require_file "Check-in-2-Solution.py"
require_file "Check-in-3-Solution.py"
command -v python3 >/dev/null 2>&1 ||
  fail "python3 is required to verify classroom starters"

for check_in in 2 3; do
  starter="Check-in-${check_in}-Starter.py"
  solution="Check-in-${check_in}-Solution.py"

  python3 -c \
    'import ast, pathlib, sys; path = pathlib.Path(sys.argv[1]); ast.parse(path.read_text(), filename=str(path))' \
    "${starter}" ||
    fail "${starter} is not valid Python syntax"
  grep -q "TODO:" "${starter}" ||
    fail "${starter} must preserve labeled student work"
  if cmp -s "${starter}" "${solution}"; then
    fail "${starter} must not duplicate the completed solution"
  fi
done

if find . \
  \( -path './.git' -o -path './node_modules' -o -path './Library' -o -path './Temp' -o -path './Logs' \) -prune -o \
  \( -name '.replit' -o -name 'replit.nix' -o -name 'replit.nix.backup' -o -name 'replit_zip_error_log.txt' \) -print | grep -q .; then
  fail "replit metadata should not be committed"
fi

source_count="$(find . \
  \( -path './.git' -o -path './node_modules' -o -path './Library' -o -path './Temp' -o -path './Logs' \) -prune -o \
  -type f \( -name '*.py' -o -name '*.java' -o -name '*.cpp' -o -name '*.c' -o -name '*.h' -o -name '*.hpp' -o -name '*.js' -o -name '*.ts' -o -name '*.swift' -o -name '*.cs' -o -name '*.md' \) -print | wc -l | tr -d ' ')"

[ "$source_count" -gt 0 ] || fail "no source-like files found"
manifest_source_count="$(
  sed -n 's/^- Source-like files: //p' COURSE_SOURCE_MANIFEST.md
)"
[ "$source_count" = "$manifest_source_count" ] ||
  fail "manifest lists ${manifest_source_count:-no} source-like files; found ${source_count}"

printf 'course source verification passed: %s source-like files\n' "$source_count"
