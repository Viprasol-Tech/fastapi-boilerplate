# Contributing to FastAPI Boilerplate

Thanks for your interest in improving this project, maintained by
[Viprasol Tech Private Limited](https://viprasol.com)! 🎉

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Before you open a pull request

Please make sure all checks pass locally — CI runs exactly these:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy src
python -m pytest
```

## Guidelines

- Keep changes focused; one logical change per pull request.
- Add or update tests for any behavioural change.
- Follow the existing code style (ruff + mypy strict are enforced).
- Write clear commit messages (Conventional Commits encouraged, e.g. `feat:`, `fix:`).
- Update the `CHANGELOG.md` under an `Unreleased` heading when relevant.

## Reporting bugs & requesting features

Use the GitHub issue templates. For security issues, please follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## Code of Conduct

By participating you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).
