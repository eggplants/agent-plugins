# commit

A Claude Code skill that reads the git diff, splits it into logical units, and
commits each one. It shows the proposed split before committing and waits for
approval.

## Installation

```text
/plugin install commit --marketplace eggplants/agent-plugins
```

For Claude Code versions before 2.1.275, follow the steps in the
[top-level README](../../README.md#installation).

## Usage

- "Commit this"
- "Split these changes into commits"
- `/commit:commit`

## Convention

| Item | Rule |
|---|---|
| Subject | `type: what changed`. The type is one of `feat`, `fix`, `refactor`, `chore`, `docs`, or `test`, with no scope |
| Length | Under 50 columns (a full-width character counts as two), with no trailing period |
| Language | The language used most in the last 10 commits. The choice is cached in the repository's `.git/commit_language` |
| Body | Rarely added. When it is, a sentence or two on why the change was made |
| First commit | `init` |
| Never added | Trailers such as `Co-Authored-By` |
| Never used | `git add -A`, `git add .`, `--no-verify` |

See [SKILL.md](skills/commit/SKILL.md) for the full text, including how changes
are split.
