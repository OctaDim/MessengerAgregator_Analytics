# Messenger Aggregator Sensitive Configuration Samples

This directory documents secret-bearing local configuration files without
storing real secrets in Git.

## Purpose

Real runtime configuration files such as root `.configs_*.ini`, root `.env`,
and `docker_compose/.env*` are intentionally ignored by Git because they can
contain API credentials, PACT API tokens, PostgreSQL passwords, MinIO keys,
SQLAdmin passwords, session signing keys, local data paths, and host-specific
deployment values.

The files in this directory are committed examples. They preserve the same file
shape, section names, parameter names, and required environment variable names
as the real local files. Values are fake but realistic, so developers and AI
agents can see the expected format without exposing real credentials, tokens,
passwords, signing keys, or local secret values.

## Layout

- `root_configs/` contains examples for root-level `.configs_*.ini` files and
  the root `.env` test-credential file.
- `docker_compose/` contains examples for Docker Compose environment files.

## Root Config Files

- `.configs_api.ini.example` - FastAPI host, port, basic API credentials, and
  Starlette/FastAPI session signing key.
- `.configs_pact_api.ini.example` - PACT API token and outbound API base URLs
  used by the local PACT helper routers.
- `.configs_postgres.ini.example` - application PostgreSQL connection values
  for each environment-selected section.
- `.configs_s3_minio.ini.example` - local S3-compatible MinIO endpoint,
  console URL, access key, secret key, and default bucket.
- `.configs_sqladmin.ini.example` - seeded SQLAdmin superadmin and admin
  credentials.
- `.env.example` - test API credentials loaded by the runtime settings module.

## Docker Compose Env Files

- `.env.postgres.example` - PostgreSQL Compose variables: database name,
  published host and port, user, password, data directory, and initdb
  arguments.
- `.env.s3_minio.example` - MinIO Compose variables: published host and ports,
  root credentials, data directory, and default bucket list.

## Parameter Notes

### FastAPI API Config

- `API_HOST` and `API_PORT` define the Uvicorn bind target.
- `API_USERNAME` and `API_PASSWORD` are basic credentials used by project
  request-auth helpers.
- `FASTAPI_SESSION_KEY` signs admin/session middleware state and must be long,
  random, and deployment-specific in real files.

### PACT API Config

- `PACT_API_TOKEN_KEY` authenticates outbound PACT API calls.
- `PACT_API_V1_BASE_URL`, `PACT_API_V2_BASE_URL`, and
  `PACT_EMERGENCY_CALL_URL` are configurable so local mock services can replace
  external PACT APIs during development.

### PostgreSQL Config

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, and
  `POSTGRES_DB_NAME` define the application database connection.
- Root `.configs_postgres.ini` values should match the active Compose env file
  when the local Docker stack is used.

### MinIO/S3 Config

- `S3_ENDPOINT_URL` and `S3_CONSOLE_URL` point to MinIO API and console
  endpoints.
- `S3_ACCESS_KEY` and `S3_SECRET_KEY` must match the MinIO root credentials
  used by Compose when local object storage is enabled.
- `S3_DEFAULT_BUCKET` is the default bucket name used by local object-storage
  workflows and webhook metadata.

### SQLAdmin Config

- `SQLADMIN_SUPERADMIN_USERNAME` and `SQLADMIN_SUPERADMIN_PASSWORD` seed the
  superadmin account.
- `SQLADMIN_ADMIN_USERNAME` and `SQLADMIN_ADMIN_PASSWORD` seed the admin
  account.

### Root Test Env

- `API_TEST_USERNAME` and `API_TEST_PASSWORD` are local test credentials read
  from `.env`.

### Compose Env Files

- `POSTGRES_DATA_DIR` and `MINIO_DATA_DIR` are host paths for persistent local
  data and must not point to source-controlled directories unless explicitly
  intended.
- `POSTGRES_INITDB_ARGS` controls PostgreSQL initialization options.
- `MINIO_DEFAULT_BUCKETS` is consumed by the bucket-init Compose job.

## Update Rules

When a real secret-bearing config file gains, removes, or renames a parameter,
update the matching sample file in the same change. Keep example values
realistic enough to show the expected format, but never copy real credentials,
tokens, passwords, cookies, signing keys, local-only secret values, or
deployment-specific secrets into this directory.

Run this contract check after updating samples:

```bash
PYENV_VERSION=3.12.13 python -m unittest _tests.sensitive_config.test_sensitive_config_samples
```
