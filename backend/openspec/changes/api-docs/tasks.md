## 1. OpenAPI Specification

- [ ] 1.1 Create `backend/docs/` directory
- [ ] 1.2 Write `backend/docs/openapi.yaml` — OpenAPI 3.0.3 spec for all 9 endpoints:
  - `GET /api/v1/auth/login`
  - `GET /api/v1/auth/callback`
  - `GET /api/v1/users/me`
  - `PATCH /api/v1/users/me`
  - `GET /api/v1/internal-providers`
  - `GET /api/v1/providers`
  - `POST /api/v1/providers`
  - `DELETE /api/v1/providers/{provider_id}`
  - `PUT /api/v1/providers/{provider_id}/default`
  - Include request/response schemas, JWT Bearer auth, example payloads
- [ ] 1.3 Add `components/securitySchemes` for `Bearer` auth

## 2. REST Client File

- [ ] 2.1 Create `http/` directory at project root
- [ ] 2.2 Write `http/rest.api.http` — VS Code REST Client file with:
  - `@baseUrl` variable pointing to `http://localhost:8000`
  - Dev login request that captures `Authorization` header token
  - Named requests for each endpoint using captured token
  - Example request bodies for POST/PATCH endpoints
