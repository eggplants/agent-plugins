---
name: copilot-review
description: "Fetch the unresolved GitHub Copilot review comments on a pull request, check each one against the current code, agree on a course of action with the user (fix, decline, defer to an issue, or skip), then fix, commit, reply, and resolve the thread. Use when the user asks to address, handle, or go through Copilot's review comments on a PR. Takes an optional PR number or URL; defaults to the PR for the current branch."
argument-hint: "[PR number | PR URL]"
---

# Copilot Review

Work through the unresolved review threads that GitHub Copilot left on a pull
request, one at a time: verify each comment, agree on a course of action with
the user, and carry it out. Posting replies, resolving threads, pushing, and
creating issues all wait for the user's confirmation.

## Steps

### 1. Pick the pull request

Use the PR number or URL given as an argument; otherwise use the PR for the
current branch.

```bash
gh pr view [<number> | <url>] --json number,url,state,headRefName
```

If there is no PR, say so and stop.

In the `gh` commands below, `gh` fills in `{owner}` and `{repo}` from the
repository in the current directory. When the URL points to a PR in another
repository, prefix every command with `GH_REPO=OWNER/REPO`.

Before changing any code, check with `git branch --show-current` that the local
branch matches the PR's `headRefName`. If it does not, ask the user whether to
run `gh pr checkout <number>`.

### 2. Fetch the review threads

Replace `PR_NUMBER` with the actual number. This prints one JSON object per
line, for each unresolved thread whose first comment is from Copilot.

```bash
gh api graphql --paginate \
  -F owner='{owner}' -F repo='{repo}' -F number=PR_NUMBER \
  -f query='
query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 50) {
            nodes { databaseId author { login } body diffHunk createdAt }
          }
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved | not)
  | select(.comments.nodes[0].author.login == "copilot-pull-request-reviewer")'
```

Use `reviewThreads`, not `reviews`: it gives each thread's resolved state and
both of the IDs the later steps need.

| Value | Shape | Used in |
|---|---|---|
| `id` | String starting with `PRRT_` | Step 9, resolving the thread |
| `databaseId` of the first comment | Number | Step 8, replying (REST API) |

A comment's GraphQL `id` (a string starting with `PRRC_`) does not work with the
REST reply endpoint. Copilot's login is `copilot-pull-request-reviewer` in
GraphQL but `Copilot` in the REST API.

### 3. List the comments

If there are no matching threads, tell the user there are no unresolved Copilot
review comments and stop.

Otherwise show the count and a numbered list with each thread's `path:line` and
the first line of its comment. Mark the threads whose `isOutdated` is `true`.

### 4. Learn the repository's ground rules

Before the first thread, read these once:

- Conventions: whichever of `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`,
  `.github/copilot-instructions.md`, and `README.md` exist
- Format, lint, and test commands: tasks in `mise.toml`, `scripts` in
  `package.json`, `Makefile`, `justfile`, `pyproject.toml`, and the CI under
  `.github/workflows/`
- The commit message convention, and where work is tracked (GitHub Issues, or
  an external tracker such as Linear or Jira)

Use them when verifying comments in step 5 and when checking changes from step
6 on.

### 5. Handle each thread

For each thread, in order:

1. Show the full comment, `path:line`, and `diffHunk`. If the thread already has
   replies, show them too
2. Read the file and check whether the comment applies to the current code
3. Report what you found, recommend a course of action, and ask the user to
   choose one:
   - **Fix**: go through step 6, then implement the fix
   - **Decline**: write down why the comment does not apply and draft a reply.
     Include a link to official documentation that backs this up, if there is
     one
   - **Defer**: the comment is valid but out of scope for this PR. Create an
     issue in the tracker found in step 4 and reply that it will be handled
     there
   - **Skip**: do nothing and move on
   - **Discuss**: talk the comment through with the user

A Copilot comment can be right in general and still not apply to this
repository: the code may reproduce the behavior of an existing system, follow
an external constraint, or be a deliberate design choice. Never accept a
comment without the check in item 2.

If the comment contains a `suggestion` code block (a change Copilot proposes),
treat it as a candidate fix. Do not apply it as is; verify it like any other
fix.

### 6. Check the impact of a fix

Before implementing a fix, check:

- **Blast radius**: grep for the callers of the function, module, config, or
  shared role or module being changed. A change to a shared piece reaches
  everything that uses it
- **Per-environment files**: when files are split per environment (`dev`,
  `stg`, `prod`, ...), do not fix one and leave the others out of step
- **Generated files**: for comments on lockfiles or generated code, fix the
  source (config or code) instead of editing the output
- **Breaking changes**: for changes that replace or destroy resources in
  infrastructure as code, break the compatibility of a public API or schema, or
  restart services, estimate the impact (downtime, data loss), tell the user,
  and ask before going ahead
- **Already applied**: if an environment has already been deployed or applied,
  fixing the code is not enough; it has to be applied again. Tell the user
- **Secrets**: prioritize verifying comments about credential handling or
  permissions

### 7. Verify and commit the fixes

Run the format, lint, and test commands found in step 4 and make sure they
pass. If they fail, fix the problem before moving on.

Checks that need credentials or access to live environments (`terraform plan`,
`ansible-playbook --check`, diffs against a cloud environment, ...) are for the
user to run; ask them to. If such output is pasted in the PR description,
suggest updating the description as well.

Commit the fixes following the repository's commit convention, using the
`commit` skill if it is available. Note the hash of each commit:

```bash
git rev-parse --short HEAD
```

The replies refer to the commits, so ask the user before pushing, and push
once they approve, before posting any reply.

### 8. Reply

Draft a reply for each thread with a decided course of action, show all drafts
together, and post them once the user approves. Do not reply to skipped
threads.

Use the `databaseId` of the thread's first comment as `COMMENT_DATABASE_ID`.
Leaving `PR_NUMBER` out of the path returns 404.

```bash
gh api 'repos/{owner}/{repo}/pulls/PR_NUMBER/comments/COMMENT_DATABASE_ID/replies' \
  -X POST -F body=@- <<'EOF'
Reply body
EOF
```

Do not put the body in `-f body="..."`: replies contain backticks and quotes,
which break shell quoting. Pass it on standard input through a heredoc with a
quoted delimiter (`<<'EOF'`), as above.

Write each reply in the language of the Copilot comment it answers. Depending
on the course of action, include:

- **Fix**: one or two sentences on what was changed and how, and the commit
  hash. Write the hash as plain text, not in backticks, and separate it from
  the preceding punctuation with a space (also after full-width punctuation
  such as `。`)

  ```text
  Included all arguments in the cache key. abc1234
  ```

- **Decline**: why the comment does not apply. If there is a documentation URL
  to back it up, put it first

  ```text
  https://docs.example.com/reference/option

  The default already behaves this way, so setting it explicitly is unnecessary.
  ```

- **Defer**: the URL of the issue that was created and when it is planned

### 9. Resolve the threads

Among the threads that got a reply, resolve the ones that are settled (fixed,
declined, or deferred), after confirming with the user. Use the thread's `id`
from step 2 (the value starting with `PRRT_`) as `THREAD_ID`.

```bash
gh api graphql -f threadId=THREAD_ID -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { isResolved }
  }
}'
```

Leave threads with an ongoing discussion unresolved.

### 10. Summarize

Report how many threads were fixed, declined, deferred, and skipped, how many
replies were posted, and how many threads were resolved.

## Notes

- A comment with `line: null` is about the whole file or about a line that no
  longer exists. Use `diffHunk` to find the context
- A thread with `isOutdated: true` points at lines that later commits changed.
  Read the current file and decide whether the comment still holds
- `diffHunk` is only an excerpt with surrounding context lines. Always read the
  actual file before fixing anything
- Copilot's review summary (the long body of the review itself) is out of
  scope. Handle only the comments attached to lines
- For comments on encrypted files or files holding secrets, never paste
  decrypted content or secret values into a reply. If the comment is a
  misreading of ciphertext, reply that the file is encrypted and resolve the
  thread
- For "this is usually written like X" comments on config or code carried over
  from an existing system, the first question is whether the change would alter
  the existing behavior
