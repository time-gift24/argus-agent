# Provider Streaming Validation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Change provider connectivity tests to validate streaming support using streaming requests, while preserving the current REST response contract for the frontend.

**Architecture:** The backend keeps the same provider test endpoints and response schema, but the provider test service switches from non-streaming `invoke()` to a streaming-first probe. Success is defined as opening the stream and receiving the first meaningful chunk; failures remain redacted and categorized for debugging.

**Tech Stack:** FastAPI, Python 3.12, langchain-openai, pytest

---

### Task 1: Convert service tests from invoke-based assumptions to stream-based assumptions

**Files:**
- Modify: `backend/tests/test_provider_test.py`

**Step 1: Write the failing tests**

- Update the fake LLM test double so it supports a streaming method instead of only `invoke()`.
- Add a test proving the probe returns success only after receiving the first streamed chunk.
- Add a test proving empty/no-op chunks do not count as success.
- Keep the existing redaction tests and adapt them to stream initialization failures.

**Step 2: Run test to verify it fails**

Run: `uv run python -m pytest -q tests/test_provider_test.py`
Expected: FAIL because the production code still uses `invoke()`

**Step 3: Commit**

```bash
git add backend/tests/test_provider_test.py
git commit -m "test: define streaming provider probe behavior"
```

### Task 2: Implement streaming-first provider probe

**Files:**
- Modify: `backend/app/services/provider_test.py`
- Test: `backend/tests/test_provider_test.py`

**Step 1: Write minimal implementation**

- Replace the internal probe logic so it opens a stream from `ChatOpenAI`.
- Iterate only until the first meaningful chunk is received.
- Measure latency to first chunk.
- Stop reading immediately after success.
- Preserve safe error normalization.

**Step 2: Run focused tests**

Run: `uv run python -m pytest -q tests/test_provider_test.py`
Expected: PASS

**Step 3: Commit**

```bash
git add backend/app/services/provider_test.py backend/tests/test_provider_test.py
git commit -m "feat: validate provider streaming capability"
```

### Task 3: Verify endpoint regressions

**Files:**
- Modify: none expected
- Test: `backend/tests/test_providers.py`

**Step 1: Run provider regression tests**

Run: `uv run python -m pytest -q tests/test_providers.py`
Expected: PASS

**Step 2: Run both suites together**

Run: `uv run python -m pytest -q tests/test_provider_test.py tests/test_providers.py`
Expected: PASS

**Step 3: Commit**

```bash
git add backend/app/services/provider_test.py backend/tests/test_provider_test.py
git commit -m "test: verify streaming provider probe regressions"
```

### Task 4: Manual validation in dev UI

**Files:**
- Modify: none expected

**Step 1: Start backend and frontend**

Run:

```bash
cd backend && make dev
cd frontend && npm run dev
```

Expected:
- backend listens on `127.0.0.1:8000`
- frontend listens on `localhost:5173`

**Step 2: Validate streaming-compatible provider**

- Open `http://localhost:5173/`
- Login in dev mode
- Go to provider create form
- Use an OpenAI-compatible streaming provider config
- Click `测试连接`

Expected:
- success response if first streamed chunk arrives
- latency reflects time-to-first-chunk

**Step 3: Validate non-compatible or wrong-model cases**

- Retry with an incompatible endpoint or invalid model

Expected:
- safe categorized failure message
- no leaked API key, URL path, or raw upstream exception

**Step 4: Commit**

```bash
git add backend/app/services/provider_test.py backend/tests/test_provider_test.py
git commit -m "feat: complete streaming provider validation"
```
