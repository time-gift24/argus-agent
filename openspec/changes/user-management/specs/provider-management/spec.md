## ADDED Requirements

### Requirement: User can list all internal providers

The system SHALL allow authenticated users to list all `kind=internal` providers via `GET /internal-providers`.

#### Scenario: Successful listing
- **WHEN** authenticated user makes `GET /internal-providers`
- **THEN** system responds with HTTP 200 and JSON array of all internal providers; each item contains `id`, `name`, `kind`, `created_at`; `config` field is NEVER returned

#### Scenario: Unauthenticated listing
- **WHEN** unauthenticated user makes `GET /internal-providers`
- **THEN** system responds with HTTP 401

---

### Requirement: User can list own providers

The system SHALL allow authenticated users to list their own (kind=user) provider associations via `GET /providers`.

#### Scenario: Successful listing
- **WHEN** authenticated user makes `GET /providers`
- **THEN** system responds with HTTP 200 and JSON array; each item contains `id`, `name`, `kind`, `is_default`, `created_at` from UserProvider join Provider; `config` field is NEVER returned

#### Scenario: User with no providers
- **WHEN** authenticated user has no associated providers
- **THEN** system responds with HTTP 200 and empty JSON array `[]`

---

### Requirement: User can create a user provider

The system SHALL allow authenticated users to create a user provider via `POST /providers`.

#### Scenario: Successful creation
- **WHEN** authenticated user makes `POST /providers` with body `{"name": "My OpenAI", "config": {"api_key": "...", "base_url": "..."}}`
- **THEN** system creates a new Provider (kind=user) with config encrypted via AES-256-GCM, creates a UserProvider association with `is_default=false`, responds with HTTP 201 and provider object (config excluded)

#### Scenario: Config encryption
- **WHEN** user creates a provider with `POST /providers`
- **THEN** the `config` field in DB SHALL be AES-256-GCM encrypted; system stores `base64(iv || ciphertext || tag)`

#### Scenario: First provider becomes default
- **WHEN** user has zero providers and creates their first provider
- **THEN** the new UserProvider association SHALL have `is_default=true`

#### Scenario: Invalid config missing api_key
- **WHEN** user makes `POST /providers` with body missing `config.api_key`
- **THEN** system responds with HTTP 422 and validation error

---

### Requirement: User can delete own provider

The system SHALL allow authenticated users to delete their provider association via `DELETE /providers/{provider_id}`.

#### Scenario: Successful deletion
- **WHEN** authenticated user makes `DELETE /providers/{provider_id}` where the association exists
- **THEN** system deletes the UserProvider row (NOT the Provider row, since it may be shared), responds with HTTP 204

#### Scenario: Deleting another user's provider
- **WHEN** authenticated user makes `DELETE /providers/{provider_id}` for a provider not associated with them
- **THEN** system responds with HTTP 404

#### Scenario: Deleting internal provider is forbidden
- **WHEN** authenticated user makes `DELETE /providers/{provider_id}` for a provider with `kind=internal`
- **THEN** system responds with HTTP 403

---

### Requirement: User can set default provider

The system SHALL allow authenticated users to set their default provider via `PUT /providers/{provider_id}/default`.

#### Scenario: Successful default update
- **WHEN** authenticated user makes `PUT /providers/{provider_id}/default` for an associated provider
- **THEN** system sets `is_default=false` for all their other UserProvider rows, sets `is_default=true` for this one, responds with HTTP 200

#### Scenario: Setting non-associated provider as default
- **WHEN** user makes `PUT /providers/{provider_id}/default` for a provider not associated with them
- **THEN** system responds with HTTP 404

---

### Requirement: Provider config is never exposed via API

The system SHALL NEVER return `config` field in any API response for any provider type.

#### Scenario: Config excluded from list response
- **WHEN** user retrieves providers via `GET /providers` or `GET /internal-providers`
- **THEN** the response SHALL NOT contain a `config` key

#### Scenario: Config excluded from create response
- **WHEN** user creates a provider via `POST /providers`
- **THEN** the response SHALL NOT contain a `config` key

---

### Requirement: Internal providers are seeded on startup

The system SHALL upsert all `Kind.INTERNAL` providers defined in code on application startup.

#### Scenario: Startup upsert
- **WHEN** application starts
- **THEN** for each internal Provider defined in code, system checks if it exists in DB by (name, kind); if not, INSERT; if exists, do nothing

#### Scenario: Internal provider config is encrypted
- **WHEN** internal provider is upserted
- **THEN** the `config` field SHALL also be AES-256-GCM encrypted (even if currently empty, for future extensibility)
