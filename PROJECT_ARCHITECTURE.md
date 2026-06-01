Created by: Codex
Date: 2026-06-01

# Project Architecture

## Project Overview

AI Messenger Aggregator Analytics is a Python/FastAPI service for receiving,
normalizing, storing, and inspecting messenger-related webhook data. The project
aggregates events from two API surfaces:

- PACT API webhooks and helper endpoints for conversations, messages, companies,
  and emergency-call workflows.
- Global messenger aggregator webhooks for normalized message events.

The service persists webhook and reference data in PostgreSQL, exposes selected
data through FastAPI routers, and provides an SQLAdmin-based administrative
panel for operators.

## Runtime Entry Point

- `main.py` is the application entry point.
- `create_fastapi_application()` creates the FastAPI app, includes routers,
  configures SQLAdmin, and wraps the app with Starlette `SessionMiddleware`.
- The FastAPI lifespan startup currently calls `run_postgres()` as a placeholder
  and creates default SQLAdmin users. Shutdown disposes async and sync
  PostgreSQL engines.
- When executed as a script, `main.py` initializes PostgreSQL tables with
  SQLAlchemy metadata and then starts Uvicorn.

## High-Level Directory Structure

```text
.
|-- main.py                         # FastAPI app factory, router registration, SQLAdmin setup, Uvicorn startup.
|-- requirements.txt                # Pinned Python dependencies.
|-- PROJECT_ARCHITECTURE.md         # Current AI-agent architecture reference.
|-- .gitignore                      # Ignore rules for virtualenvs, IDE files, caches, local data, and scratch files.
|-- .configs_api.ini                # API host, port, credentials, and session-key settings.
|-- .configs_pact_api.ini           # PACT API token and outbound local API base URL settings.
|-- .configs_postgres.ini           # PostgreSQL connection settings.
|-- .configs_s3_minio.ini           # Local MinIO/S3 endpoint and bucket settings.
|-- .configs_sqladmin.ini           # SQLAdmin default credential settings.
|-- .env                            # Test API credentials loaded by settings.
|-- .agents/                        # Local agent metadata directory; currently no project files inside.
|-- .codex/                         # Local Codex metadata directory; currently no project files inside.
|-- .venv3145/                      # Local virtual environment, ignored and not part of application architecture.
|-- _tests/                         # Centralized test tree mirroring tested Python packages and infrastructure areas.
|-- admin_panel/                    # SQLAdmin views, auth backend, templates, filters, and custom actions.
|-- configs/                        # Runtime settings, enums, labels, filters, and console-color constants.
|-- db_postgres/                    # SQLAlchemy models, connections, sessions, queries, and initialization.
|-- docker_compose/                 # PostgreSQL and MinIO Compose stacks, runbooks, and env files.
|-- fast_api/                       # FastAPI routers and Pydantic request/response schemas.
|-- meta_classes/                   # Shared metaclasses, currently SingletonMeta for DB connection classes.
|-- utils_common/                   # General utility helpers for paths, validation, hashing, serialization, etc.
|-- utils_specific/                 # Domain-specific event-data enrichment helpers.
|-- _docs/                          # Deployment notes and SIP call examples.
```

## Key Modules

### FastAPI Application

- `main.py` registers active routers from `fast_api/` and
  `fast_api/_pact_fastapi_aps/`.
- `fast_api/app_root_url/router_main.py` redirects `/` to `/docs`.
- `fast_api/app_global_api_health_check/` exposes a global API health-check
  route.
- `fast_api/app_global_api_webhooks/` accepts normalized global messenger
  webhook events, validates them with Pydantic, enriches event data, and stores
  rows in PostgreSQL. Its schemas include base event/user data, raw events,
  message lifecycle events, callback/inline/chat-action events, and optional
  S3 attachment metadata.
- `fast_api/app_get_paginated_messages/` exposes paginated message retrieval for
  a web account.
- `fast_api/app_web_account/` contains the shared web-account request schema
  used by paginated message retrieval. It is not a standalone router.
- `fast_api/app_test_endpoint/` contains a development-only test endpoint.
- `fast_api/_pact_fastapi_aps/` contains PACT-specific routers for webhooks,
  messages by conversation, message data by ID, conversation data by ID,
  all conversations, all companies, and emergency-call requests.

### Admin Panel

- `admin_panel/admin_views/` defines SQLAdmin model views for conversations,
  messages, chat subjects, plus keywords, and minus keywords.
- `admin_panel/admin_views/admin_auth_role_backend.py` implements SQLAdmin login
  against `AuthRoleModel` in PostgreSQL.
- `admin_panel/custom_templates/sqladmin/_pact_sqladmin_/` overrides SQLAdmin
  templates for list, edit, create, details, login, layout, and error pages.
- `configs/filters.py` and `admin_panel/custom_classes/` provide custom filter
  behavior for the admin UI.

### PostgreSQL Layer

- `db_postgres/postgres_conn/pgs_connection.py` owns singleton sync and async
  SQLAlchemy engines.
- `db_postgres/postgres_conn/postgres_session.py` provides sync and async
  context managers that commit on success, roll back on errors, and close
  sessions.
- `db_postgres/postgres_init/declarative_base_model.py` defines the SQLAlchemy
  declarative `Base`.
- `db_postgres/postgres_init/db_tables_initialization.py` imports all models and
  creates tables from metadata.
- `db_postgres/postgres_models/` contains shared models such as customers,
  global webhooks, and admin auth roles.
- `db_postgres/postgres_models/_pact_pgs_models/` contains PACT domain models:
  webhook auth, conversations, messages, attachments, reactions, audio
  transcriptions, plus/minus keywords, and chat subjects.
- `db_postgres/postgres_queries/` and `db_postgres/postgres_queries_utils/`
  contain domain and reusable query helpers.

### Configuration

- `configs/settings.py` is the central runtime configuration module.
- Settings are read from `.env` and multiple INI files in the repository root.
- API and PostgreSQL config sections are selected by detected external IP,
  platform, and predefined config names.
- The root `.configs_*.ini` files are configured for local development through
  `127.0.0.1`: the FastAPI service binds to localhost, PostgreSQL points to the
  host-published Compose port from `docker_compose/.env.postgres`, MinIO points
  to the host-published Compose API/console ports from
  `docker_compose/.env.s3_minio`, and outbound PACT/emergency-call base URLs are
  read from `.configs_pact_api.ini`.
- The module probes internal and external IP addresses during import. Be careful
  when using broad import checks in offline or sandboxed environments because
  this side effect can make otherwise static checks environment-sensitive.
- Option dataclasses such as `FASTAPI_OPTIONS`, `ALCHEMY_OPTIONS`,
  `PACT_WEBHOOKS_OPTIONS`, `PACT_SQLADMIN_OPTIONS`, and
  `GLOBAL_API_WEBHOOKS_OPTIONS` group runtime flags.
- `S3_ENDPOINT_URL`, `S3_CONSOLE_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, and
  `S3_DEFAULT_BUCKET` are loaded from `.configs_s3_minio.ini`; current runtime
  code mainly persists incoming S3 metadata from webhook payloads, while MinIO
  provisioning is handled by Docker Compose/runbooks.
- Root-level `.configs_*.ini`, `.env`, and `docker_compose/.env.*` files are
  operational inputs and may contain secrets. Document paths and required keys,
  not concrete secret values.

### Docker Infrastructure

- `docker_compose/docker-compose_postgres.yaml` defines a PostgreSQL 16 stack
  with a one-shot directory-init service, bind-mounted persistent storage,
  `pg_isready` healthcheck, resource documentation, and log rotation.
- `docker_compose/docker-compose_s3_minio.yaml` defines a MinIO stack with
  directory initialization, MinIO readiness checks, and a bucket-init job.
- `docker_compose/.env.postgres` and `docker_compose/.env.s3_minio` provide the
  Compose-specific local environment files expected by the runbooks. Treat them
  as sensitive local configuration.
- `docker_compose/POSTGRES_RUNBOOK.md` and
  `docker_compose/S3_MINIO_RUNBOOK.md` document validation and startup commands.
- `docker_compose/_backup/docker-compose.yaml` is retained as backup material,
  not the active Compose contract. Prefer the explicit PostgreSQL and MinIO
  Compose files above for current infrastructure work.

### Test Tree

- `_tests/` is the centralized test location. Runtime packages should not keep
  `test_*.py` files beside application modules.
- `_tests/configs/test_local_config_contract.py` validates root-localhost INI
  settings against the Docker Compose env files without importing
  network-sensitive runtime settings.
- `_tests/docker_compose/test_compose_configs.py` provides unittest-based
  contract tests for the Compose files and runbooks.
- `_tests/fast_api/_pact_fastapi_aps/` mirrors PACT FastAPI packages and keeps
  endpoint-oriented test scripts beside the tested package path under `_tests`.
- `_tests/db_postgres/postgres_tests/` contains PostgreSQL query/model
  integration test scripts.

## Main Data Flow

1. External systems send webhook requests to FastAPI routes.
2. Routers validate request payloads with Pydantic schemas.
3. Auth data is verified through simple username/password helpers where the
   endpoint requires it.
4. Event data is normalized or enriched by router logic and helper functions.
5. SQLAlchemy async sessions persist new or updated ORM rows.
6. SQLAdmin reads and manages the persisted records through configured admin
   views.

## AI Agent Development Guide

Use this section as the first routing map when changing the project.

### Change Impact Map

- **New public API endpoint:** add or update a feature package under
  `fast_api/` or `fast_api/_pact_fastapi_aps/`, define/update Pydantic schemas,
  register the router in `main.py`, then update the API surface summary in this
  file.
- **Webhook payload change:** update the relevant Pydantic scheme, router
  normalization logic, persistence model/query helpers, and any admin view that
  displays the changed data.
- **New PostgreSQL table/model:** add the ORM model under
  `db_postgres/postgres_models/` or `_pact_pgs_models/`, import it through
  `db_postgres/postgres_init/db_tables_init_imports.py`, add query helpers when
  reused, and document the new model here.
- **Database query behavior:** prefer extending `db_postgres/postgres_queries/`
  or `db_postgres/postgres_queries_utils/` instead of embedding reusable query
  logic in routers.
- **Admin panel behavior:** update `admin_panel/admin_views/` for model view
  behavior, `admin_panel/custom_templates/` for rendered SQLAdmin pages, and
  `configs/filters.py` or `admin_panel/custom_classes/` for filtering behavior.
- **Runtime configuration:** update `configs/settings.py` and the relevant
  `.configs_*.ini` or `.env*` file together. Never print or document secret
  values.
- **Docker infrastructure:** update the Compose file, matching runbook, and
  `_tests/docker_compose/test_compose_configs.py` in the same change.
- **Tests:** put new tests under `_tests/<tested-package-path>/` rather than
  inside runtime packages. Mirror the tested package path where practical.

### Safe Exploration Order

1. Read `PROJECT_ARCHITECTURE.md` before changing code.
2. Read `main.py` to understand registered routers and startup behavior.
3. Read the feature router and its schema module.
4. Follow persistence from router to query helper to ORM model.
5. Check admin views if the changed data is operator-visible.
6. Run the narrowest relevant tests and record any environment limitation.

### Verification Levels

- **Static contract check:** use stdlib-only tests such as
  `PYENV_VERSION=3.12.13 python -m unittest _tests.docker_compose.test_compose_configs`
  when Docker or database access is unavailable.
- **Application import check:** import or instantiate only the target module if
  dependencies and config files are available. Be careful because
  `configs/settings.py` reads local INI files and probes IP information during
  import.
- **Documentation sync check:** after changing structure or behavior, read
  `PROJECT_ARCHITECTURE.md` and update affected sections in the same change.
- **Database-backed check:** run query/model tests only when PostgreSQL is
  reachable and the local `.configs_postgres.ini` points at the intended
  database.
- **Runtime infrastructure check:** for PostgreSQL and MinIO startup claims, run
  the runbook `docker-compose ... config --quiet`, `up -d`, `ps`, logs, and
  healthcheck commands from `docker_compose/` on a Docker-enabled machine.

### Current Operational Caveats

- `run_postgres()` and `run_redis()` in `main.py` are placeholders and do not
  start external services.
- Root-level `.configs_*.ini`, `.env`, and Docker Compose env files are local
  operational inputs. Do not expose their secret values in final answers,
  documentation, tests, or logs.
- Global API message payloads can carry S3 metadata (`s3_bucket`, `s3_key`,
  `s3_endpoint`, `s3_uri`). The project stores those fields but does not yet
  contain a dedicated S3 client abstraction.
- Some PACT routers are implemented but not included in `main.py`. Treat router
  registration as the source of truth for the public FastAPI surface.
- The project currently creates tables from SQLAlchemy metadata. There is no
  Alembic migration history in this snapshot, so schema changes need extra care.
- Several tests likely require live PostgreSQL or external API assumptions.
  Prefer narrow tests first and clearly separate static confidence from runtime
  proof.
- `.agents/` and `.codex/` exist as local metadata directories but currently do
  not contain project instructions or code files in this workspace snapshot.
- `.venv3145/`, `.idea/`, caches, and generated bytecode are local workspace
  artifacts and should not be used as architecture evidence.

## API Surface Summary

Active routers registered by `main.py`:

- `GET /` redirects to `/docs`.
- `POST /aggregator_api/webhooks_1/` receives PACT webhook data.
- `POST /aggregator_api/pct_all_conversations/` requests PACT conversations.
- `POST /aggregator_api/conversation_messages/` requests messages by
  conversation.
- `POST /aggregator_api/message_data_by_id/` requests one PACT message by ID.
- `POST /global_msg_aggregator/global_api_webhooks/` receives normalized global
  aggregator webhook events.
- `POST /global_msg_aggregator/global_api_health_check` checks global API
  health.
- `POST /global_msg_aggregator/all_messages` returns paginated message data.
- `POST /develop_test_endpoint/develop_test_endpoint/` is a development route.

Some PACT routers exist but are not currently registered in `main.py`, including
all-companies, conversation-data-by-ID, and emergency-call routers. They are
imported by other PACT workflows and can be registered explicitly if they should
be exposed as public API endpoints.

`fast_api/app_web_account/` is intentionally schema-only in this snapshot: it
validates `web_account_id` and `web_account_username` for
`POST /global_msg_aggregator/all_messages`.

## Architecture Patterns

- **Application factory:** `create_fastapi_application()` builds the runtime app
  and middleware stack.
- **Router-per-feature:** FastAPI routers are grouped by integration surface and
  use case.
- **Pydantic validation boundary:** Incoming API payloads are validated before
  domain processing and persistence.
- **Repository/query helpers:** Database operations are extracted into focused
  query utility modules.
- **SQLAlchemy unit-of-work style sessions:** Session context managers own
  commit, rollback, and close behavior.
- **Singleton database engines:** Sync and async SQLAlchemy engine wrappers use
  `SingletonMeta` to avoid repeatedly creating engine objects.
- **Config-by-environment files:** Runtime values are loaded from INI files and
  `.env` rather than hard-coded directly in routers.
- **Config-driven outbound API URLs:** PACT and emergency-call outbound URLs are
  composed from settings so local mock services can replace external APIs during
  development without editing routers.
- **Admin UI over ORM models:** SQLAdmin model views expose operational data
  management without a separate frontend.
- **Compose startup contract tests:** Infrastructure expectations are tested by
  checking stable fragments in Compose files and runbooks.

## Technology Stack

- Python application stack with FastAPI `0.123.7`, Starlette `0.50.0`, and
  Uvicorn `0.38.0`.
- Pydantic v2 for request models and validation.
- SQLAlchemy `2.0.45` with `asyncpg` for async PostgreSQL access and
  `psycopg2` for sync initialization/access.
- PostgreSQL 16 via Docker Compose for the primary relational database.
- SQLAdmin `0.22.0` with Jinja2/WTForms for the admin panel.
- MinIO via Docker Compose for S3-compatible object storage infrastructure.
- HTTPX/AIOHTTP for outbound HTTP workflows.
- Telethon, aio-pika, QR-code helpers, Pillow, and SQLite async support are
  installed in `requirements.txt`; this snapshot does not show an active
  registered runtime integration point for them.
- bcrypt-based password hashing helpers.
- unittest for existing infrastructure contract tests.

## Architecture Decision Records

### ADR-001: FastAPI as the API Framework

FastAPI is used because the service is API-first, relies on request validation,
and benefits from async handlers for webhook and outbound API workflows. It also
keeps OpenAPI documentation available during development through `/docs`.

### ADR-002: PostgreSQL as the Primary Store

PostgreSQL is used because webhook analytics data is relational: conversations,
messages, attachments, auth events, keywords, and admin roles need structured
queries, filtering, ordering, and durable persistence. This fits better than a
simple key-value cache for the current operational and admin-panel needs.

### ADR-003: SQLAlchemy Sync and Async Engines

The project keeps both async and sync SQLAlchemy engines. Async sessions support
FastAPI request handlers, while sync access is used for startup-time table
initialization and compatibility with synchronous maintenance flows.

### ADR-004: SQLAdmin for Operational Back Office

SQLAdmin is used instead of a custom frontend so operators can inspect and edit
ORM-backed data quickly while staying close to the database model definitions.

### ADR-005: INI and `.env` Configuration

The project uses root-level INI files plus `.env` because several deployment
targets are selected by IP/platform and because credentials must stay outside
router and model code. AI agents must treat these files as sensitive local
configuration and avoid exposing secrets in logs or documentation.

### ADR-006: Docker Compose Init Services for Storage

PostgreSQL and MinIO Compose stacks use one-shot init services to validate host
directories before starting stateful services. This makes startup failures
clearer than letting the main service fail later with an opaque storage error.

### ADR-007: Contract Tests for Compose Files

The Compose stacks are tested with lightweight unittest fragment checks. This is
not a replacement for live Docker startup validation, but it prevents accidental
removal of important startup, healthcheck, runbook, and environment contracts.

### ADR-008: Localhost-First Development Configuration

Root `.configs_*.ini` values are kept localhost-first for this workspace so the
FastAPI app, PostgreSQL, MinIO, and local mocks for external APIs can run on one
developer machine. PostgreSQL and MinIO values mirror the host-published ports
from the Docker Compose env files, while outbound PACT URLs stay configurable so
the same routers can target local mocks or real APIs by configuration only.

## Accepted Conventions

- Keep comments, annotations, and commented notes in code in English only.
- Keep `PROJECT_ARCHITECTURE.md` synchronized whenever code, structure,
  infrastructure, or major documentation changes.
- Keep the first two lines of `PROJECT_ARCHITECTURE.md` as `Created by:` and
  `Date:` with the latest update date.
- Prefer existing project patterns before introducing new abstractions.
- Add new FastAPI routes in a feature package with a router module and Pydantic
  schema module where appropriate.
- Register only intended public routers in `main.py`.
- Keep PostgreSQL model imports wired through
  `db_postgres/postgres_init/db_tables_init_imports.py` so metadata-based table
  initialization sees new models.
- Use query helper modules for reusable database operations instead of embedding
  complex SQLAlchemy logic directly in routers.
- Treat root `.configs_*.ini` and `.env` files as sensitive operational config.
- Do not commit local virtual environments, IDE state, caches, bytecode, or
  generated scratch files.
- For Docker Compose changes, update the corresponding runbook and contract
  tests together.

## Testing and Verification

Existing test locations:

- `_tests/configs/test_local_config_contract.py` validates that local root INI
  files use localhost and match Compose-published PostgreSQL and MinIO settings.
- `_tests/docker_compose/test_compose_configs.py` validates Docker Compose and
  runbook contracts.
- `_tests/db_postgres/postgres_tests/` contains PostgreSQL query/model tests.
- `_tests/fast_api/_pact_fastapi_aps/` contains endpoint-oriented PACT FastAPI
  test modules.

Recommended checks:

```bash
PYENV_VERSION=3.12.13 python -m unittest _tests.configs.test_local_config_contract
PYENV_VERSION=3.12.13 python -m unittest _tests.docker_compose.test_compose_configs
PYENV_VERSION=3.12.13 python -m unittest discover -s _tests -t . -p "test_*.py"
```

In this workspace, a plain `python` command may fail if pyenv has no global
Python version selected. Use the explicit `PYENV_VERSION` prefix above or select
an appropriate local Python version before running tests.

For database-dependent tests, ensure PostgreSQL configuration files and a live
database are available before running the broader test set.

## Recommendations for Future Work

- Replace placeholder `run_postgres()` with an explicit readiness check or
  remove it if Docker/process orchestration is intentionally external.
- Register or remove currently unregistered PACT routers to make the public API
  surface unambiguous.
- Move sensitive root INI and `.env` files to deployment-managed secrets or
  document which files are local-only examples.
- Add automated tests for `create_fastapi_application()` router registration and
  SQLAdmin setup.
- Add a dedicated S3 client/service layer before introducing code that reads or
  writes MinIO objects directly; this will keep webhook persistence separate
  from object-storage access.
- Remove unused dependencies or document their planned integration paths once
  Telethon, aio-pika, QR-code, Pillow, or SQLite workflows become active.
- Consider adding Alembic migrations before production schema changes become
  frequent. Current table creation is metadata-driven and does not provide
  versioned migrations.
- Document the expected PostgreSQL and MinIO env-file names directly beside the
  Compose files and keep runbooks as the operational source of truth.

## Detailed Documentation Links

- PostgreSQL Compose runbook: `docker_compose/POSTGRES_RUNBOOK.md`
- MinIO Compose runbook: `docker_compose/S3_MINIO_RUNBOOK.md`
- Linux service notes: `_docs/_docs_server_linux/`
- SIP call example: `_docs/_doc_sip_call_example/sip_call.txt`
