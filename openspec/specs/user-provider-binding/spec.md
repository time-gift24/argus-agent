# user-provider-binding Specification

## Purpose
定义 User 与 user Provider 之间的绑定及默认策略。

## Requirements
### Requirement: UserProvider junction links user to kind=user provider

The system SHALL create a UserProvider record when a user creates their first user provider.

#### Scenario: First provider creates junction
- **WHEN** user creates their first provider via `POST /providers`
- **THEN** system creates both a Provider row (kind=user) and a UserProvider row linking them

#### Scenario: Subsequent providers extend junction
- **WHEN** user creates additional providers via `POST /providers`
- **THEN** system creates a new Provider row and a new UserProvider row linking to the same user

---

### Requirement: User has exactly one default provider at all times

The system SHALL maintain exactly one `is_default=true` UserProvider record per user whenever the user has at least one provider.

#### Scenario: Default is set on first provider
- **WHEN** user creates their first provider
- **THEN** `is_default=true`

#### Scenario: Switching default clears previous
- **WHEN** user calls `PUT /providers/{id}/default` to set a new default
- **THEN** all other UserProvider rows for that user have `is_default=false`

#### Scenario: Deleting default provider reassigns default
- **WHEN** user deletes the provider with `is_default=true`
- **THEN** system sets `is_default=true` on the remaining provider with the most recent `created_at`; if no providers remain, no row has `is_default=true`

---

### Requirement: UserProvider only applies to kind=user providers

The system SHALL NOT create UserProvider records for `kind=internal` providers.

#### Scenario: Internal providers are not linked
- **WHEN** an agent or service references an internal provider by `provider_id`
- **THEN** the query SHALL NOT join through UserProvider; internal providers are globally accessible without user association

#### Scenario: User cannot delete internal provider via junction
- **WHEN** user attempts `DELETE /providers/{internal_provider_id}`
- **THEN** system responds with HTTP 403 (handled at API layer, not at junction)
