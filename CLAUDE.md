# CodeReviewer Agent — instructions for AI coding agents

Read `README.md` first for product context, including features, architecture, stack, and
roadmap.

## Current status

Milestone M0 provides a runnable FastAPI webhook backbone. When asked to "help build the
system" without more specific instructions, start with the earliest unfinished milestone in
the README roadmap (currently M1) and continue in order.

## Working principles

- **Complete one milestone at a time.** Deliver something runnable or demonstrable at the
  end of each milestone instead of building every agent at once.
- **Never auto-merge or auto-approve.** This is a hard boundary: the tool may only write
  comments and suggestions. It must never change pull request status or merge anything
  automatically.
- **Reduce noise.** Suppressing a low-confidence finding is better than posting an incorrect
  suggestion that causes developers to lose trust in automated reviews.
- **Follow the selected stack** in the README unless the user explicitly requests a change.
- **Language**: Use English for code, commit messages, and product documentation.

## Architecture changes

The blueprint is an initial plan, not an immutable rule. If there is a strong technical reason
to take a different approach, explain the tradeoffs to the user before making the change.
