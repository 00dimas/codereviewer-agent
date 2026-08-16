# CodeReviewer Agent

An automated multi-agent system for reviewing GitHub pull requests, detecting bugs,
performing security checks, and suggesting improvements.

> Status: **Blueprint** — no code has been implemented yet.

## Overview

A multi-agent system that connects to GitHub webhooks, analyzes pull request diffs, and
provides structured reviews covering logic bugs, potential vulnerabilities, and code
simplification opportunities. It works like a senior reviewer while remaining automated
and consistent across every pull request.

## Key features

- **Trigger**: A GitHub App/webhook listens for pull request open and update events, then
  fetches the diff through the GitHub API
- **Bug-hunter agent**: Identifies logic errors and overlooked edge cases
- **Security agent**: Detects risky patterns such as injection, committed secrets, and
  authentication bypasses
- **Style/simplify agent**: Suggests simplifications without changing behavior
- **Router**: Selects agents based on file type and skips lockfiles and generated files
- **Output**: Posts structured, severity-tagged, line-level pull request comments
- **Confidence gating**: Suppresses low-confidence findings to reduce noise

## Architecture

```
PR event → Fetch diff → Route ke agent (bug / security / style)
  → Aggregate findings → Post PR comment
```

## Stack (free tier)

| Layer | Component |
|---|---|
| Integration | GitHub App (Probot/Octokit) |
| LLM | Groq / Gemini API (free tier) |
| Backend | FastAPI webhook receiver |
| Storage | PostgreSQL (review and finding logs) |
| CI and self-testing | GitHub Actions |

## Roadmap

| # | Milestone |
|---|---|
| M0 | Set up the GitHub App and a stub webhook receiver |
| M1 | Run the bug-hunter agent against a sample diff |
| M2 | Add security and style agents with finding aggregation |
| M3 | Deploy and test against a small open-source repository |
| M4 | Tune confidence thresholds and reduce false positives |

## Note

This tool provides **suggestions only** and never has authority to approve or merge pull
requests. Final decisions always remain with human reviewers. GitHub API rate limits must
be respected.
