# user-auth Specification

## Purpose
定义 OIDC 与开发模式下的认证流程。

## Requirements
### Requirement: OIDC login redirects to provider

The system SHALL redirect unauthenticated users to the configured OIDC Provider's authorization endpoint when they access `GET /auth/login`.

#### Scenario: Successful redirect
- **WHEN** unauthenticated user navigates to `GET /auth/login` with `?redirect_uri=<uri>`
- **THEN** system redirects with HTTP 302 to OIDC authorization URL containing `client_id`, `redirect_uri`, `response_type=code`, `scope=openid profile email`, and a random `state` stored in session

#### Scenario: Dev mode skips redirect
- **WHEN** `DEV_MODE=true` and user navigates to `GET /auth/login`
- **THEN** system redirects with HTTP 302 directly to `/auth/callback?code=dev&state=dev`

---

### Requirement: OIDC callback exchanges code for user info

The system SHALL handle `GET /auth/callback` by exchanging the authorization code for tokens, fetching user info, upserting the user, and issuing a JWT.

#### Scenario: Production callback
- **WHEN** `DEV_MODE=false` and OIDC Provider returns to `/auth/callback?code=<code>&state=<state>`
- **THEN** system exchanges code for tokens, fetches userinfo from `{issuer}/userinfo`, upserts User (by oauth_provider + oauth_subject), and responds with `{token: <jwt>, token_type: "Bearer"}`

#### Scenario: Dev callback with valid header
- **WHEN** `DEV_MODE=true` and request includes `X-Dev-User: <name>` header
- **THEN** system skips OIDC exchange, constructs FakeUserInfo with name, upserts User, and responds with `{token: <jwt>, token_type: "Bearer"}`

#### Scenario: Dev callback without header
- **WHEN** `DEV_MODE=true` and request does NOT include `X-Dev-User` header
- **THEN** system responds with HTTP 400 and error `"X-Dev-User header required in dev mode"`

#### Scenario: Invalid state parameter
- **WHEN** callback receives a `state` that does not match stored session value
- **THEN** system responds with HTTP 400 and error `"Invalid state parameter"`

---

### Requirement: JWT protects authenticated endpoints

The system SHALL enforce JWT authentication on all endpoints decorated with `requires_auth`, using the `Authorization: Bearer <token>` header.

#### Scenario: Valid JWT grants access
- **WHEN** request includes `Authorization: Bearer <valid_jwt>` header where JWT is signed by `JWT_SECRET` and not expired
- **THEN** request proceeds with `request.state.user_id` set from JWT sub

#### Scenario: Missing Authorization header
- **WHEN** request to protected endpoint omits `Authorization` header
- **THEN** system responds with HTTP 401 and error `"Missing Authorization header"`

#### Scenario: Expired JWT
- **WHEN** request includes a JWT that is signed correctly but past `exp`
- **THEN** system responds with HTTP 401 and error `"Token expired"`

#### Scenario: Malformed JWT
- **WHEN** request includes a JWT that is not valid HS256 or not a valid JWT at all
- **THEN** system responds with HTTP 401 and error `"Invalid token"`

---

### Requirement: JWT payload structure

The JWT issued by the system SHALL contain the following claims:
- `sub`: user's UUID string
- `name`: user's display name
- `exp`: expiration timestamp (24h from issuance)
- `iat`: issued-at timestamp

#### Scenario: JWT contains required claims
- **WHEN** system issues a JWT after successful OIDC callback
- **THEN** the JWT payload SHALL contain `sub`, `name`, `exp`, `iat` fields

---

### Requirement: Dev mode requires explicit environment flag

The system SHALL treat any `DEV_MODE` value other than the literal string `"true"` as production mode.

#### Scenario: Dev mode is off by default
- **WHEN** `DEV_MODE` environment variable is not set or set to any value other than `"true"`
- **THEN** system SHALL operate in production mode (OIDC flow required)

#### Scenario: Dev mode activates only with explicit true
- **WHEN** `DEV_MODE` environment variable is set to `"true"`
- **THEN** system SHALL enable dev mode bypass
