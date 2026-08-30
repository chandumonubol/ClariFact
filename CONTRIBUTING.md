# Contributing to ClariFact

Thank you for considering contributing to ClariFact! This project is built by a four-member team and aims to be safe for multiple AI coding agents to work on in parallel.

## Branching Strategy
- Always work on a **feature branch** off `main`.
- Recommended branch names: `feature/backend`, `feature/ai`, `feature/frontend`, `feature/database`.
- Never make uncontrolled changes to another member's area without a PR.
- Merge through pull requests only.

## Commit Conventions
- Use present tense: "Add claim extraction", not "Added claim extraction".
- Use imperative mood: "Fix authentication middleware".
- Prefix scope with area: `auth/`, `ai/`, `frontend/`, `db/`.
- Example: `auth: add bcrypt password hashing`, `ai: train claim classifier`.

## Pull Request Expectations
- All PRs must include:
  - Clear description of what changed and why.
  - Link to relevant task in `TASK_TRACKER.md`.
  - Update to `API_CONTRACT.md` if APIs changed.
  - Update to `DECISIONS.md` if architecture changed.
  - Update to `DATABASE_STATE.md` if schema changed.
  - Update to `AI_STATE.md` if AI components changed.
  - Screenshots or diff highlights for UI changes.
- Minimum 1 reviewer required (team member not owning the area).
- All relevant tests must pass.
- Documentation must be synchronized with implementation.

## Testing Requirements
- New features must include unit tests.
- Critical paths (auth, analysis pipeline) must have integration tests.
- Model evaluation: claim classifier F1 >= 0.65 on held-out test set.
- Run `pytest` and `npm test` before submitting PR.

## Code Style
- Backend: Black formatter, isort imports, type annotations where practical.
- Frontend: ESLint + Prettier configured.
- Import order: standard library → third party → local.
- No hardcoded secrets, passwords, or API keys.
- Use `.env` variables for all configuration.

## Documentation Updates
- Whenever implementation changes, update relevant agent state files:
  - `agent/CURRENT_STATE.md`
  - `agent/TASK_TRACKER.md`
  - `agent/CHANGELOG.md`
- If architectural decision changes: update `agent/DECISIONS.md`.
- If API changes: update `agent/API_CONTRACT.md`.
- If database structure changes: update `agent/DATABASE_STATE.md` and `docs/BACKEND_SCHEMA.md`.
- If AI implementation changes: update `agent/AI_STATE.md`.

## Agent Context Update Requirements
- Do NOT read the entire repository on every task.
- Read `AGENTS.md` first, then `agent/PROJECT_CONTEXT.md`, then `agent/CURRENT_STATE.md`, then relevant sections of `TASK_TRACKER.md`.
- Read `DECISIONS.md` before changing architecture.
- Read `API_CONTRACT.md` before changing APIs.
- Read `DATABASE_STATE.md` before changing database structure.
- Read `AI_STATE.md` before modifying AI components.
- Only then inspect implementation files necessary for the task.

## Getting Started
1. Read `AGENTS.md`.
2. Read `agent/PROJECT_CONTEXT.md`.
3. Read `agent/CURRENT_STATE.md`.
4. Check `agent/TASK_TRACKER.md` for open tasks.
5. Choose a feature branch name matching your area.
6. Implement, test, and submit a PR.

## Questions?
Open an issue or discuss on the team channel. Refer to the documentation files for answers.