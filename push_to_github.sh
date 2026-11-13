#!/usr/bin/env bash
# Save pending work in logical commits, then push the existing history.
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
repo_url='https://github.com/ArijitGuha0179/26AI60R04-project1.git'

if [[ "${1:-}" == '--help' ]]; then
    echo 'Usage: bash push_to_github.sh'
    echo 'Commits pending project changes in groups and pushes to origin/main.'
    echo 'Existing commits are preserved. No force push is used.'
    exit 0
fi
if (( $# > 0 )); then
    echo 'Unknown argument. Use --help.' >&2
    exit 1
fi

git rev-parse --show-toplevel >/dev/null
if [[ -n "$(git diff --cached --name-only)" ]]; then
    echo 'Some files are already staged. Commit or unstage them before running this script.' >&2
    exit 1
fi
if ! git var GIT_AUTHOR_IDENT >/dev/null 2>&1; then
    echo 'Configure your commit identity, then run this script again:' >&2
    echo '  git config user.name "ArijitGuha0179"' >&2
    echo '  git config user.email "YOUR_GITHUB_EMAIL"' >&2
    exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
    if [[ "$(git remote get-url origin)" != "$repo_url" ]]; then
        echo 'origin points to a different repository. Check git remote -v first.' >&2
        exit 1
    fi
    if [[ "$(git remote get-url --push origin)" != "$repo_url" ]]; then
        echo 'origin has a different push URL. Check git remote -v first.' >&2
        exit 1
    fi
else
    git remote add origin "$repo_url"
fi

commit_group() {
    local message="$1"
    shift
    local -a paths=()
    local path
    for path in "$@"; do
        if [[ -e "$path" ]] || git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
            paths+=("$path")
        fi
    done
    if (( ${#paths[@]} == 0 )); then
        return
    fi
    git add -- "${paths[@]}"
    if ! git diff --cached --quiet; then
        git commit -m "$message"
    else
        echo "No pending changes: $message"
    fi
}

commit_group 'Update project setup and documentation' \
    .gitignore README.md requirements.txt problem_statement.pdf push_to_github.sh
commit_group 'Update source data and reproduction tools' data tools reproduce.py
commit_group 'Update contributor chart and data' fig1-contributors
commit_group 'Update weekly commits chart and data' fig2-commits
commit_group 'Update code frequency chart and data' fig3-code-frequency
commit_group 'Update top committers chart and data' fig4-top-committers
commit_group 'Update LaTeX report and validation' main.tex main.pdf validation.json

# Checkpoint files in tmp-check are committed separately when instructed.
echo 'Commits to publish:'
git log --oneline -10
git push -u origin HEAD:main
echo "Published to $repo_url"
