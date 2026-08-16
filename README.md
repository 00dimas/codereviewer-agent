# CodeReviewer Agent

An automated multi-agent system for reviewing GitHub pull requests, detecting bugs,
performing security checks, and suggesting improvements.

> Status: **M0 backbone complete** — webhook ingestion is ready; review agents are not yet
> implemented.

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
PR event → Fetch diff → Route to agent (bug / security / style)
  → Aggregate findings → Post PR comment
```

The current M0 implementation covers the first boundary: receiving GitHub webhook events,
verifying their signatures, and classifying supported pull request actions.

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

## Getting started

### Requirements

- Python 3.9 or newer
- A GitHub webhook secret

### Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
export GITHUB_WEBHOOK_SECRET="replace-with-the-same-secret-used-by-github"
uvicorn code_reviewer.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive documentation at
`http://127.0.0.1:8000/docs`.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Report service health and environment |
| `POST` | `/webhooks/github` | Verify and accept GitHub webhook deliveries |

The webhook receiver accepts `opened`, `reopened`, and `synchronize` pull request actions.
Other events are acknowledged and ignored so GitHub does not retry them unnecessarily.

### Configuration

| Variable | Default | Purpose |
|---|---|---|
| `APP_ENV` | `development` | Runtime environment name |
| `LOG_LEVEL` | `INFO` | Application log level |
| `GITHUB_WEBHOOK_SECRET` | none | Secret used to verify `X-Hub-Signature-256` |

### Development checks

```bash
ruff check .
pytest
```

## Note

This tool provides **suggestions only** and never has authority to approve or merge pull
requests. Final decisions always remain with human reviewers. GitHub API rate limits must
be respected.
