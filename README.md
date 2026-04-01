# StorageVoice AI

Production-oriented, multi-tenant backend scaffold for a voice + automation platform for self-storage operators.

## Design goals

- Start with UnitTrac support immediately.
- Future-proof for any storage software provider with an API.
- Keep provider-specific logic isolated behind a stable interface.
- Support secure tenant onboarding with encrypted API credential storage.

## Current scaffold

- FastAPI API service for tenant onboarding/configuration
- Provider adapter architecture:
  - `StorageProvider` interface (provider-agnostic contract)
  - `UnitTracProvider` implementation
  - registry/factory for dynamic provider selection
- Encrypted credential storage service
- Initial endpoints:
  - list supported providers
  - create tenant and provider config
  - validate provider credentials

## Quick start

1. Create env file:
   - `cp .env.example .env`
2. Install:
   - `pip install -e .`
3. Run API:
   - `uvicorn apps.api_service.src.main:app --reload --host 0.0.0.0 --port 8000`

## Database migrations (PostgreSQL)

- Configure `DATABASE_URL` in `.env`
- Run migrations:
  - `alembic upgrade head`
- Current core tables:
  - `tenants`
  - `tenant_provider_configs`
  - `operator_contacts`
  - `audit_logs`

## Why provider adapters?

New management software support should only require:

1. Add a new provider package implementing `StorageProvider`.
2. Register it in `providers/registry/factory.py`.
3. Optionally add provider-specific validation schema.

No core routing or business logic rewrite needed.

## GitHub: CI and syncing

- **CI**: Pushes and pull requests to `main` run [GitHub Actions](.github/workflows/ci.yml) (install, Ruff, pytest).
- **Dependency updates**: [Dependabot](.github/dependabot.yml) opens weekly pip PRs and monthly Actions updates.
- **Push changes in one step** (after you commit locally, or it will commit for you):

```bash
./scripts/sync-push.sh "your commit message"
```

Cursor/VS Code does not auto-push to GitHub; use the script above or **Source Control → Sync** / `git push` after saving.
