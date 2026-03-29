# Provider Streaming Validation Design

**Goal:** Make provider connectivity testing validate streaming capability instead of non-streaming `invoke()` calls, while keeping the frontend API contract unchanged.

## Scope

- Keep existing endpoints:
  - `POST /api/v1/providers/test-config`
  - `POST /api/v1/providers/{provider_id}/test`
- Keep existing response shape:
  - `{ success, message, latency_ms }`
- Change backend internals so test success means:
  - the provider accepted a streaming chat request
  - the backend received at least one valid streamed chunk

## Approach

The backend provider test service will switch from `ChatOpenAI.invoke()` to a streaming-first probe. The probe will open a stream, read until the first meaningful chunk arrives, then stop immediately and return success with measured latency. This keeps the UI simple while validating the exact capability the product requires.

## Error Handling

- Continue redacting upstream errors.
- Keep failure messages diagnostic but safe.
- Distinguish between:
  - auth failure
  - network/base URL failure
  - non OpenAI-compatible endpoint
  - model/parameter incompatibility
  - rate limit / temporary upstream failure
  - generic streaming initialization failure

## Testing

- Unit-test the streaming probe behavior with a fake `ChatOpenAI`.
- Verify success only when a streamed chunk is actually observed.
- Verify stream setup failures are normalized and redacted.
- Re-run provider API regression tests to ensure endpoint behavior stays stable.
