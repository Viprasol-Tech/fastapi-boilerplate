<p align="center"><img src="docs/assets/logo.png" width="120"></p>

# FastAPI Boilerplate

> A production-ready FastAPI starter — app factory, typed config, versioned API, auth, CRUD, structured logging, and an offline test-suite.

*Built and maintained by [Viprasol Tech](https://viprasol.com) — Fintech Experts. Full-Stack Builders.*

[![CI](https://img.shields.io/github/actions/workflow/status/Viprasol-Tech/fastapi-boilerplate/ci.yml?branch=main&style=flat-square)](https://github.com/Viprasol-Tech/fastapi-boilerplate/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue?style=flat-square)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/lint-ruff-261230?style=flat-square)](https://github.com/astral-sh/ruff)
[![Telegram](https://img.shields.io/badge/Telegram-help-26A5E4?style=flat-square&logo=telegram)](https://t.me/viprasol_help)
[![Stars](https://img.shields.io/github/stars/Viprasol-Tech/fastapi-boilerplate?style=flat-square)](https://github.com/Viprasol-Tech/fastapi-boilerplate/stargazers)

---

A clean, opinionated foundation for shipping FastAPI services fast — without inheriting someone else's framework. Everything runs and tests **fully offline** via FastAPI's `TestClient`; there is no database or network dependency to fight before you write your first endpoint.

## ✨ Features

- 🏭 **App factory** (`create_app`) for clean, testable wiring and per-environment overrides.
- ⚙️ **Typed configuration** with `pydantic-settings` (env vars + `.env`, cached singleton).
- 🧭 **Versioned API** mounted at `/api/v1` with a tidy, extensible router layout.
- 📦 **Example CRUD resource** backed by a swappable repository interface (in-memory by default).
- 🔐 **API-key auth dependency** via the `X-API-Key` header.
- 🪵 **Structured JSON logging** — machine-parseable, zero extra dependencies.
- 🧯 **Global exception handlers** with a uniform error envelope (never leaks internals).
- ❤️ **Health & readiness** probes (`/health`, `/ready`) ready for Kubernetes.
- 📄 **Pagination helper** with validated `page`/`size` query parameters.
- 🌐 **CORS** preconfigured and environment-driven.
- 🧪 **14 offline tests** covering CRUD, auth, validation and health.
- 🐳 **Docker & docker-compose** for one-command local runs.
- 🛠️ **Strict tooling**: ruff, mypy `--strict`, pytest, and a cross-platform CI matrix.

## 🚀 Quickstart

### Docker (recommended)

```bash
docker compose up --build
# API: http://localhost:8000  ·  Docs: http://localhost:8000/docs
```

### Local (Python 3.11+)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Run the dev server
uvicorn app.main:app --reload --app-dir src

# Or drive it offline — no server needed
python examples/usage.py
```

## 🧑‍💻 Usage

Create an item (writes require an API key):

```bash
curl -X POST http://localhost:8000/api/v1/items \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Starter Plan", "price": 49.0}'
```

List items (paginated, public):

```bash
curl "http://localhost:8000/api/v1/items?page=1&size=20"
```

Swap the in-memory store for your own backend by implementing the `ItemRepository`
protocol in `src/app/repository.py` and overriding the `get_repository` dependency.

## 🗺️ Roadmap

- [ ] SQLAlchemy + Alembic repository implementation.
- [ ] JWT / OAuth2 auth option alongside API keys.
- [ ] Rate limiting middleware.
- [ ] OpenTelemetry tracing hooks.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our
[Code of Conduct](CODE_OF_CONDUCT.md) before opening a pull request.

## 📬 Contact — Viprasol Tech Private Limited

- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech — fintech software, algorithmic trading systems, MT4/MT5 bots, AI voice agents, and B2B SaaS. Need a custom build? [Get in touch](mailto:support@viprasol.com).*

## 📄 License

Released under the [MIT License](LICENSE) — © 2025 Viprasol Tech Private Limited.
