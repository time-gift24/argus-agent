## Context

All 9 user management API endpoints are implemented but undocumented in machine-readable form. Existing implementation lives in `backend/app/api/endpoints/`.

## Goals / Non-Goals

**Goals:**
- Emit `backend/docs/openapi.yaml` conforming to OpenAPI 3.0.3
- Emit `http/rest.api.http` for VS Code REST Client

**Non-Goals:**
- No code generation from spec
- No Swagger UI hosting (can be added separately)
- No breaking changes to existing endpoints

## Decisions

**D1: OpenAPI output as standalone YAML file**
- Keep spec alongside code in `backend/docs/openapi.yaml`
- Alternative: use FastAPI built-in `/openapi.json` — not used because this file is version-controlled and available offline

**D2: `.http` file at project root**
- `http/rest.api.http` at repo root for easy discovery
- Use `http/` directory to group REST testing assets
- VS Code REST Client extension consumes `.http` files natively

**D3: Dev-mode auth in `.http` file**
- Use `X-Dev-User` header for all authenticated requests
- Store base URL as a `@baseUrl` variable at file top

## Risks / Trade-offs

- OpenAPI spec is hand-written — must be kept in sync when endpoints change (no CI enforcement in this change)
