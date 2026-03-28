## Why

The user management module is implemented but lacks machine-readable API documentation. OpenAPI 3.0.3 spec enables client code generation, interactive documentation (Swagger UI, Redoc), and postman/insomnia import. An `.http` file provides zero-setup local testing via VS Code REST Client.

## What Changes

- Generate `backend/docs/openapi.yaml` — complete OpenAPI 3.0.3 specification covering all 9 implemented endpoints
- Generate `http/rest.api.http` — VS Code REST Client file for local API testing with dev-mode shortcuts

## Capabilities

### New Capabilities

- `api-documentation`: OpenAPI 3.0.3 spec documenting all auth, user, and provider endpoints with request/response schemas, auth requirements, and example payloads

## Impact

- New file: `backend/docs/openapi.yaml`
- New file: `http/rest.api.http` (at project root)
