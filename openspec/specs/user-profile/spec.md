# user-profile Specification

## Purpose
定义用户自助资料读取与更新 API 行为。

## Requirements
### Requirement: Authenticated user can retrieve own profile

The system SHALL allow authenticated users to retrieve their own profile via `GET /me`.

#### Scenario: Successful profile retrieval
- **WHEN** authenticated user makes `GET /me` request
- **THEN** system responds with HTTP 200 and JSON body containing `id`, `name`, `oauth_provider`, `meta_data`, `created_at`, `updated_at`

#### Scenario: Unauthenticated profile access
- **WHEN** unauthenticated user makes `GET /me` request (no valid JWT)
- **THEN** system responds with HTTP 401 and error `"Missing Authorization header"`

---

### Requirement: Authenticated user can update own display name

The system SHALL allow authenticated users to update their `name` via `PATCH /me`.

#### Scenario: Successful name update
- **WHEN** authenticated user makes `PATCH /me` with body `{"name": "New Name"}`
- **THEN** system updates the user's name in DB, responds with HTTP 200 and updated user object

#### Scenario: Update with empty name
- **WHEN** authenticated user makes `PATCH /me` with body `{"name": ""}`
- **THEN** system responds with HTTP 422 and validation error `"name cannot be empty"`

#### Scenario: Patch other fields is ignored
- **WHEN** authenticated user makes `PATCH /me` with body `{"id": "fake-id"}` or `{"oauth_provider": "evil"}`
- **THEN** system ignores those fields, updates only `name`, responds with HTTP 200

---

### Requirement: User creation on first OIDC login

The system SHALL automatically create a user record on first OIDC login (upsert by oauth_provider + oauth_subject).

#### Scenario: New user upsert
- **WHEN** OIDC callback receives userinfo for a (oauth_provider, oauth_subject) pair not yet in DB
- **THEN** system creates a new User with name from OIDC userinfo, oauth_provider, oauth_subject, and current timestamps

#### Scenario: Existing user upsert
- **WHEN** OIDC callback receives userinfo for a (oauth_provider, oauth_subject) pair already in DB
- **THEN** system updates `updated_at`, does NOT overwrite `name` (user may have changed it locally)

#### Scenario: Name from OIDC on first login
- **WHEN** a new user is created during OIDC callback
- **THEN** the user's `name` SHALL be populated from OIDC userinfo `name` or `preferred_username` or `login` field (first available)
