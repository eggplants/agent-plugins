# copilot-review

A Claude Code skill that works through the unresolved GitHub Copilot review
comments on a pull request: it checks each one against the current code, then
fixes, commits, replies, and resolves the thread. It asks for confirmation
before pushing, posting replies, and resolving threads.

## Installation

```text
/plugin install copilot-review --marketplace eggplants/agent-plugins
```

For Claude Code versions before 2.1.275, follow the steps in the
[top-level README](../../README.md#installation).

## Usage

| Request | What it does |
|---|---|
| "Address Copilot's review comments" | Targets the PR for the current branch |
| `/copilot-review:copilot-review 123` | Targets PR #123 |
| `/copilot-review:copilot-review https://github.com/acme/app/pull/123` | Targets the PR at the URL |

## Flow

1. Pull the unresolved threads whose first comment is from Copilot, using the
   GraphQL `reviewThreads` field
2. Read the repository's conventions (`CLAUDE.md`, `AGENTS.md`,
   `CONTRIBUTING.md`, ...) and find its format, lint, and test commands
3. For each thread, check whether the comment applies to the current code,
   recommend a course of action, and ask whether to fix, decline, defer to an
   issue, skip, or discuss it
4. After fixing, run the lint and test commands, commit, and push once the user
   approves
5. Show all reply drafts together, post them once the user approves (each in
   the language of the Copilot comment it answers), and resolve the settled
   threads

See [SKILL.md](skills/copilot-review/SKILL.md) for the full procedure.

## Requirements

- [GitHub CLI](https://cli.github.com/) (`gh`), logged in with permission to
  comment on pull requests and resolve review threads in the target repository
