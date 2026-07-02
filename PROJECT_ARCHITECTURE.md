Created by: Codex
Date: 2026-07-02
Time: 13:56:24 +0300

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
|-- .gitignore                      # Ignore rules for virtualenvs, IDE files, caches, local data, scratch files, and local VS Code workspace settings.
|-- .configs_api.ini                # API host, port, credentials, and session-key settings.
|-- .configs_pact_api.ini           # PACT API token and outbound local API base URL settings.
|-- .configs_postgres.ini           # PostgreSQL connection settings.
|-- .configs_s3_minio.ini           # Local MinIO/S3 endpoint and bucket settings.
|-- .configs_sqladmin.ini           # SQLAdmin default credential settings.
|-- .env                            # Test API credentials loaded by settings.
|-- .agents/                        # Local agent metadata directory; currently no project files inside.
|-- .codex/                         # Local Codex metadata directory; currently no project files inside.
|-- .idea/                          # Local PyCharm metadata; not part of runtime architecture.
|-- .venv31211/, .venv3145/         # Local virtual environments; ignored and not part of application architecture.
|-- TEMP_MINIO_FILES/               # Local object-storage scratch/download data; may contain sensitive files and is not source.
|-- _tests/                         # Centralized test tree mirroring tested Python packages and infrastructure areas.
|-- admin_panel/                    # SQLAdmin views, auth backend, templates, filters, and custom actions.
|-- configs/                        # Runtime settings, enums, labels, filters, and console-color constants.
|-- db_postgres/                    # SQLAlchemy models, connections, sessions, queries, and initialization.
|-- docker_compose/                 # Local/IP Docker Compose stacks, runbooks, env files, and backup compose files.
|-- fast_api/                       # FastAPI routers and Pydantic request/response schemas.
|-- meta_classes/                   # Shared metaclasses, currently SingletonMeta for DB connection classes.
|-- utils_common/                   # General utility helpers for paths, validation, hashing, serialization, etc.
|-- utils_specific/                 # Domain-specific event-data enrichment helpers.
|-- zExamples/                      # Experimental Telethon/update examples and local SQLite data; not active runtime code.
|-- _docs/                          # Deployment notes and SIP call examples.
|   |-- msgs_aggreg_sensitive_config_samples/ # Safe committed examples for secret-bearing local config files.
```

## Key Modules

### FastAPI Application

- `main.py` registers the active public routers from `fast_api/` and selected
  packages under `fast_api/_pact_fastapi_aps/`. Router registration in
  `routers_list` is the source of truth for the exposed FastAPI surface.
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
- `fast_api/app_get_dialog_messages_archive/` exposes archive-thread retrieval
  for one selected dialog using web-account identity, Telethon config name, and
  normalized peer identifiers.
- `fast_api/app_web_account/` contains the shared web-account request schema
  used by paginated message retrieval. It is not a standalone router.
- `fast_api/app_test_endpoint/` contains a development-only test endpoint.
- `fast_api/_pact_fastapi_aps/` contains PACT-specific routers for webhooks,
  messages by conversation, message data by ID, conversation data by ID,
  all conversations, all companies, and emergency-call requests. In the current
  `main.py` snapshot, only webhooks, all conversations, messages by
  conversation, and message data by ID are registered.

### Dialogs Archive API v1

Dialogs API v1 is intentionally split across services:

- TLT manager owns live dialog enumeration, live message polling, and sending.
- MessengerAgregator Analytics owns persisted archive retrieval for older
  normalized dialog history.

Current Dialogs-archive modules:

- `fast_api/app_get_dialog_messages_archive/`
- `db_postgres/postgres_queries/qry_get_dialog_messages_archive.py`
- `_tests/fast_api/test_dialog_messages_archive_contract.py`

#### `POST /{WEBHOOKS_GLOBAL_API_URL_BASE_NAME}/dialog_messages_archive`

- Request body:
  - `auth_data.username`: `str`, required.
  - `auth_data.password`: `str`, required.
  - `web_account_data.web_account_id`: `str`, required.
  - `web_account_data.web_account_username`: `str`, required.
  - `dialog_request_data.messenger_type`: `str`, required by contract;
    current supported value in the broader feature is `"telegram"`.
  - `dialog_request_data.config_name`: `str`, required.
  - `dialog_request_data.peer_id`: `int`, required.
  - `dialog_request_data.peer_type`: `str`, required for cross-service
    contract stability.
  - `dialog_request_data.peer_storage_type`: `str`, required; expected values:
    `user`, `chat`, `channel`.
  - `dialog_request_data.messages_limit`: `int`, optional, default `200`,
    must be positive.
  - `dialog_request_data.before_archive_id`: `int | null`, optional.
- Response:
  - `message`: `str`.
  - `messenger_type`: `str`.
  - `config_name`: `str`.
  - `peer_id`: `int`.
  - `peer_type`: `str`.
  - `peer_storage_type`: `str`.
  - `messages_limit`: `int`.
  - `before_archive_id`: `int | null`.
  - `returned_count`: `int`.
  - `has_older`: `bool`.
  - `next_before_archive_id`: `int | null`.
  - `archive_messages`: `list[archive_message]`.
- `archive_message` fields:
  - `archive_id`: `int`.
  - `message_id`: `int | null`.
  - `action`: `str | null`.
  - `event_type`: `str | null`.
  - `config_name`: `str | null`.
  - `peer_id`: `int | null`.
  - `peer_storage_type`: `str`.
  - `text`: `str`.
  - `raw_text`: `str`.
  - `old_text`: `str | null`.
  - `message_difference`: `str | null`.
  - `chat_title`: `str | null`.
  - `old_chat_title`: `str | null`.
  - `date`: `str | null`, JSON-safe datetime.
  - `edit_date`: `str | null`, JSON-safe datetime.
  - `delete_date`: `str | null`, JSON-safe datetime.
  - `out`: `bool | null`.
  - `bot`: `bool | null`.
  - `sender_id`: `int | null`.
  - `sender_username`: `str | null`.
  - `sender_first_name`: `str | null`.
  - `sender_last_name`: `str | null`.
  - `sender_phone`: `str | null`.
  - `sender_title`: `str`.
  - `file_name`: `str | null`.
  - `extra_file_name`: `str | null`.
  - `s3_bucket`: `str | null`.
  - `s3_key`: `str | null`.
  - `s3_uri`: `str | null`.

Archive-query behavior:

- `peer_storage_type` is mapped to exactly one DB field through
  `PEER_STORAGE_TYPE_TO_MODEL_FIELD`:
  - `user -> ev_peer_id_user_id`
  - `chat -> ev_peer_id_chat_id`
  - `channel -> ev_peer_id_channel_id`
- the query always filters by `web_account_id`, `web_account_username`,
  `tlt_config_name`, and the selected peer-id field;
- rows are fetched newest-first with `limit(messages_limit + 1)` so the API can
  compute `has_older`;
- the response reverses the selected page back into ascending order for chat UI
  rendering;
- `next_before_archive_id` is the oldest returned `archive_id`, which the site
  passes back to request the next older page.

### Admin Panel

- `admin_panel/admin_views/` defines SQLAdmin model views for conversations,
  messages, chat subjects, plus keywords, and minus keywords.
- `admin_panel/admin_views/admin_auth_role_backend.py` implements SQLAdmin login
  against `AuthRoleModel` in PostgreSQL.
- `admin_panel/custom_templates/sqladmin/_pact_sqladmin_/` overrides SQLAdmin
  templates for list, edit, create, details, login, layout, and error pages.
- `configs/filters.py` and `admin_panel/custom_classes/` provide custom filter
  behavior for the admin UI.
- `admin_panel/custom_actions_mixins/_pact_custom_actions/` contains SQLAdmin
  custom action mixins, including filter-cancel and example action helpers.
- `admin_panel/admin_views/__temp/`,
  `admin_panel/custom_actions_mixins/__temp/`,
  `admin_panel/custom_classes/__temp/`, and `admin_panel/decorators/__temp/`
  are retained experimental/legacy admin code areas and are not the primary
  admin-panel contract.

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
- `db_postgres/postgres_init/db_tables_init_imports.py` is the required import
  registry for metadata-based table initialization. It intentionally imports ORM
  classes for side effects; do not auto-format away or remove imports casually.
- `db_postgres/postgres_models/` contains shared models such as customers,
  global webhooks, and admin auth roles.
- `db_postgres/postgres_models/_pact_pgs_models/` contains PACT domain models:
  webhook auth, conversations, messages, attachments, reactions, audio
  transcriptions, plus/minus keywords, and chat subjects.
- `db_postgres/postgres_queries/` and `db_postgres/postgres_queries_utils/`
  contain domain and reusable query helpers.
- `db_postgres/postgres_queries_helpers/` currently exists as a package marker
  without active helper modules.
- `db_postgres/postgres_tests/__temp/` contains older database test scripts.
  New or maintained tests should live under `_tests/db_postgres/...` instead.

### Configuration

- `configs/settings.py` is the central runtime configuration module.
- Settings are read from `.env` and multiple INI files in the repository root.
- API and PostgreSQL config sections are selected by detected external IP,
  platform, and predefined config names.
- The root `.configs_*.ini` files contain multiple environment sections for
  localhost, host-IP, and broad-bind runtime modes. Do not assume every section
  is localhost-only; select the intended section through `configs/settings.py`
  and keep secret values out of documentation. PostgreSQL, MinIO, and outbound
  PACT/emergency-call values are coordinated with local INI files and Compose
  env files, but the current workspace shows drift between some tests, samples,
  and checked-out env-file names.
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

- `docker_compose/local_docker-compose_postgres.yaml` and
  `docker_compose/ip_docker-compose_postgres.yaml` define PostgreSQL 16 stacks
  with one-shot directory-init services, bind-mounted persistent storage,
  `pg_isready` healthchecks, resource documentation, log rotation, and a
  pre-start wrapper that verifies `psql` and `pg_isready` availability.
- `docker_compose/local_docker-compose_s3_minio.yaml` and
  `docker_compose/ip_docker-compose_s3_minio.yaml` define MinIO stacks with
  directory initialization, MinIO readiness checks, and a bucket-init job.
- `docker_compose/local_docker-compose-rabbitmq_aiopika.yaml` and
  `docker_compose/ip_docker-compose-rabbitmq_aiopika.yaml` define RabbitMQ
  stacks intended for aio-pika workflows. They provide AMQP and management UI
  ports, persistent bind-mounted broker data, and RabbitMQ diagnostics
  healthchecks.
- `docker_compose/local_docker-compose_sshpass.yaml` and
  `docker_compose/ip_docker-compose_sshpass.yaml` provide development helper
  containers with `openssh-client` and `sshpass`. They do not publish inbound
  ports and should not store SSH passwords or targets in Compose files.
- Runbooks expect local env files named `.env_local_postgres`,
  `.env_local_s3_minio`, and `.env_local_rabbitmq_aiopika`; IP-bound stacks
  expect `.env.ip_postgres`, `.env.ip_s3_minio`, and
  `.env.ip_rabbitmq_aiopika`. In this workspace snapshot, only
  `docker_compose/.env` is present in the compose directory, so verify or
  recreate the runbook-specific env files before running Compose commands.
  Treat all Compose env files as sensitive local configuration.
- `docker_compose/POSTGRES_RUNBOOK.md`,
  `docker_compose/S3_MINIO_RUNBOOK.md`,
  `docker_compose/RABBITMQ_AIOPIKA_RUNBOOK.md`, and
  `docker_compose/SSHPASS_RUNBOOK.md` document validation, startup, access, and
  shutdown commands for the active stacks.
- `docker_compose/_backup/` and `docker_compose/_backup_ai/` are retained as
  backup material, not the active Compose contract. Prefer the explicit
  `local_` and `ip_` Compose files for current infrastructure work.

### Test Tree

- `_tests/` is the centralized test location. Runtime packages should not keep
  `test_*.py` files beside application modules.
- `_tests/configs/test_local_config_contract.py` validates root-localhost INI
  settings against the Docker Compose env files without importing
  network-sensitive runtime settings.
- `_tests/docker_compose/test_compose_configs.py` provides unittest-based
  contract tests for the Compose files and runbooks.
- `_tests/sensitive_config/test_sensitive_config_samples.py` verifies that the
  committed sensitive-config samples preserve the same INI sections, parameter
  names, and env variable names as local secret-bearing config files while
  excluding known real secret values.
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
  healthcheck commands from `docker_compose/` on a Docker-enabled machine. Use
  the `local_` pair for loopback-only development and the `ip_` pair only on a
  host that owns the configured public/private bind address.

### Current Operational Caveats

- `run_postgres()` and `run_redis()` in `main.py` are placeholders and do not
  start external services.
- Root-level `.configs_*.ini`, `.env`, and Docker Compose env files are local
  operational inputs. Do not expose their secret values in final answers,
  documentation, tests, or logs.
- `_docs/msgs_aggreg_sensitive_config_samples/` contains committed `.example`
  files for those sensitive inputs. Keep these samples structurally identical
  to the real local files, but never copy real tokens, passwords, signing keys,
  API credentials, or host-specific secrets into them.
- Global API message payloads can carry S3 metadata (`s3_bucket`, `s3_key`,
  `s3_endpoint`, `s3_uri`). The project stores those fields but does not yet
  contain a dedicated S3 client abstraction.
- RabbitMQ/aio-pika infrastructure is available as Docker Compose/runbook
  support, but the FastAPI app does not yet register a broker consumer or
  producer in this snapshot.
- Some PACT routers are implemented but not included in `main.py`. Treat router
  registration as the source of truth for the public FastAPI surface.
- The project currently creates tables from SQLAlchemy metadata. There is no
  Alembic migration history in this snapshot, so schema changes need extra care.
- Several tests likely require live PostgreSQL or external API assumptions.
  Prefer narrow tests first and clearly separate static confidence from runtime
  proof.
- `.agents/` and `.codex/` exist as local metadata directories but currently do
  not contain project instructions or code files in this workspace snapshot.
- `.venv31211/`, `.venv3145/`, `.idea/`, caches, generated bytecode, and
  `TEMP_MINIO_FILES/` are local workspace artifacts and should not be used as
  architecture evidence.
- `zExamples/` is an examples/scratch area for Telethon and update-routing
  experiments. Treat it as reference material only unless a task explicitly
  asks to promote that code into the runtime application.
- The repository has no `pyproject.toml`, `setup.cfg`, or `pytest.ini` in this
  snapshot. Dependency declarations are currently centralized in
  `requirements.txt`, and tests are invoked with `python -m unittest`.
- Current config-contract tests are partially stale against the checked-out
  workspace: they expect `docker_compose/.env.postgres`,
  `docker_compose/.env.s3_minio`, localhost-only API INI sections, and sample
  config sections that do not match the real root INI files. Treat these
  failures as configuration/test drift until the intended env-file naming and
  sample contract are reconciled.

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
- `POST /global_msg_aggregator/dialog_messages_archive` returns archived dialog messages with backward pagination metadata.
- `POST /develop_test_endpoint/develop_test_endpoint/` is a development route.

Some PACT routers exist but are not currently registered in `main.py`, including
all-companies, conversation-data-by-ID, and emergency-call routers. Treat them
as implemented but private/unexposed modules until they are added to
`routers_list`.

`fast_api/app_web_account/` is intentionally schema-only in this snapshot: it
validates `web_account_id` and `web_account_username` for
`POST /global_msg_aggregator/all_messages` and `POST /global_msg_aggregator/dialog_messages_archive`.

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
- **Local/IP Compose split:** infrastructure stacks have separate loopback and
  IP-bound Compose/env-file pairs so local development does not accidentally
  publish services broadly, while explicit IP-bound stacks remain available for
  hosts that own the configured address.
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
- RabbitMQ via Docker Compose for planned aio-pika message-broker workflows.
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

### ADR-010: Split Local and IP-Bound Compose Stacks

Docker Compose infrastructure is split into `local_` and `ip_` file/env pairs
so loopback development stays isolated on `127.0.0.1`, while host-specific
IP-bound exposure is an explicit operational choice. This avoids accidental
service exposure and makes the bind-address assumption visible in file names,
runbooks, and tests.

### ADR-008: Localhost-First Development Configuration

Root `.configs_*.ini` values are kept localhost-first for this workspace so the
FastAPI app, PostgreSQL, MinIO, and local mocks for external APIs can run on one
developer machine. PostgreSQL and MinIO values mirror the host-published ports
from the Docker Compose env files, while outbound PACT URLs stay configurable so
the same routers can target local mocks or real APIs by configuration only.

### ADR-009: Committed Secret-Config Samples Without Real Secrets

The repository keeps real root `.configs_*.ini`, root `.env`, and
`docker_compose/.env*` files ignored because they can contain deployment
credentials, tokens, session keys, database passwords, object-storage keys, and
local data paths. Committed examples live under
`_docs/msgs_aggreg_sensitive_config_samples/` instead. They preserve structure
and parameter names so agents and developers can bootstrap safely, while tests
guard against accidental drift and known real-secret leakage.

### ADR-011: Use analytics service as the Dialogs archive source of truth

Dialogs archive history is served from this service instead of querying Telethon
directly for older messages.

Why:

- webhook-normalized rows already live here with historical metadata such as
  old text, edit/delete timestamps, sender enrichment, and S3 file references;
- archive pagination by database id is more stable and cheaper than repeatedly
  walking live Telethon history for older pages;
- keeping archive and live responsibilities separate avoids overloading TLT
  manager with long-history storage concerns.

Consequences:

- the website must merge archive history from Analytics with live polling from
  TLT manager;
- cross-service request fields such as `messenger_type`, `config_name`,
  `peer_type`, and `peer_storage_type` must remain aligned;
- Dialogs archive tests should stay in `_tests/fast_api/` and validate the API
  contract without needing real secrets.

## Accepted Conventions

- Keep comments, annotations, and commented notes in code in English only.
- Keep `PROJECT_ARCHITECTURE.md` synchronized whenever code, structure,
  infrastructure, or major documentation changes.
- Keep the first three lines of `PROJECT_ARCHITECTURE.md` as `Created by:`,
  `Date:`, and `Time:` with the latest update date and local update time.
- Ignore root and nested `PROJECT_ARCHITECTURE.md` paths in Git to reduce
  accidental staging noise, and explicitly exclude them from commits unless a
  task specifically requires repository-level documentation changes.
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
- Treat `docker_compose/.env*` files as sensitive operational config.
- Update `_docs/msgs_aggreg_sensitive_config_samples/` whenever any
  secret-bearing local config file adds, removes, or renames sections, keys, or
  env variables.
- Do not commit local virtual environments, IDE state, caches, bytecode, or
  generated scratch files.
- For Docker Compose changes, update the corresponding runbook and contract
  tests together.
- Never analyze `zBackUp/` or `zTest/`. These directories are explicitly
  excluded from agent project analysis.
- Do not treat `zExamples/`, local virtual environments, IDE metadata, caches,
  or `TEMP_MINIO_FILES/` as source-of-truth architecture. Promote anything
  useful from those areas into the normal package structure before relying on it.

## Testing and Verification

Existing test locations:

- `_tests/configs/test_local_config_contract.py` is intended to validate that
  local root INI files use localhost and match Compose-published PostgreSQL and
  MinIO settings. In the current workspace it fails because the expected
  `.env.postgres` and `.env.s3_minio` files are absent and several API INI
  sections are not localhost-only.
- `_tests/docker_compose/test_compose_configs.py` validates Docker Compose and
  runbook contracts.
- `_tests/sensitive_config/test_sensitive_config_samples.py` validates that
  committed sensitive-config examples mirror local secret-bearing file shapes
  without known real secret values. In the current workspace it fails because
  the real root INI sections and env-file names have drifted from the committed
  `.example` samples.
- `_tests/db_postgres/postgres_tests/` contains PostgreSQL query/model tests.
- `_tests/fast_api/_pact_fastapi_aps/` contains endpoint-oriented PACT FastAPI
  test modules.

Recommended checks:

```bash
./.venv31211/bin/python -m unittest _tests.configs.test_local_config_contract
./.venv31211/bin/python -m unittest _tests.docker_compose.test_compose_configs
./.venv31211/bin/python -m unittest _tests.sensitive_config.test_sensitive_config_samples
./.venv31211/bin/python -m unittest discover -s _tests -t . -p "test_*.py"
```

In this workspace, a plain `python` command resolves to Python 2.7 when pyenv is
not active, so Python 3 tests fail at import time. Use `./.venv31211/bin/python`
or another explicit Python 3 interpreter before running tests.

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
- Document the expected PostgreSQL, MinIO, RabbitMQ, and sshpass helper file
  pairs directly beside the Compose files and keep runbooks as the operational
  source of truth.

## Detailed Documentation Links

- PostgreSQL Compose runbook: `docker_compose/POSTGRES_RUNBOOK.md`
- MinIO Compose runbook: `docker_compose/S3_MINIO_RUNBOOK.md`
- RabbitMQ aio-pika Compose runbook:
  `docker_compose/RABBITMQ_AIOPIKA_RUNBOOK.md`
- sshpass helper Compose runbook: `docker_compose/SSHPASS_RUNBOOK.md`
- Sensitive config samples:
  `_docs/msgs_aggreg_sensitive_config_samples/README.md`
- Linux service notes: `_docs/_docs_server_linux/`
- SIP call example: `_docs/_doc_sip_call_example/sip_call.txt`
