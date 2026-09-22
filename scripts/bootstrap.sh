#!/bin/sh
set -eu
umask 077

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
private_dir="$repo_root/private"
skill_dir="$repo_root/skills/apply-to-jobs"

mkdir -p "$private_dir/applications" "$private_dir/documents/samples"

if [ ! -e "$private_dir/profile.md" ]; then
  cp "$skill_dir/assets/profile.template.md" "$private_dir/profile.md"
fi

if [ ! -e "$private_dir/resume.md" ]; then
  cp "$skill_dir/assets/resume.template.md" "$private_dir/resume.md"
fi

chmod -R go-rwx "$private_dir"
printf '%s\n' "Created private workspace at $private_dir"
printf '%s\n' 'Next: fill private/profile.md and private/resume.md with truthful candidate data.'
