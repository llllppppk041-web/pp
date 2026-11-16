# Apply the v4 gateway to the complete OmniSearch app

The full v4.0.0 source ZIP keeps all original v3.9.0 app modules and includes the tested integration. This repository is the focused gateway overlay; use this checklist when applying the gateway to another checkout.

## Backend integration points

In `backend/app/main.py`:

1. Import:
   ```python
   from .services.provider_gateway import (
       ask_configured_brain,
       provider_runtime_status,
       diagnose_openai_compatible,
   )
   ```
2. Add `GET /api/providers/status` returning `provider_runtime_status()`.
3. Add a protected/local-only diagnostic route that calls `diagnose_openai_compatible()`. Do not expose it on a public unauthenticated service.
4. In the existing `POST /api/ask` handler, replace the direct call to `ask_local_brain(request)` with:
   ```python
   return await ask_configured_brain(request, local_runner=ask_local_brain)
   ```
5. Keep the original Pydantic request/response schema and JSON normalisation. The adapter must return the same `AskResponse` structure as the previous local runner.

## Frontend integration point

Before choosing Android native or browser Wllama execution, query the same-origin `/api/providers/status`. If `server_provider_selected` is true, post the existing Ask payload to `/api/ask`; otherwise retain the current local-first native/browser flow. If the status request fails, default to the original native/browser route. Never place provider keys in the frontend.

## Local BitNet setup

Use the official Microsoft BitNet repository and its current build instructions. Start `llama-server` bound to `127.0.0.1`, then set `OMNI_OPENAI_BASE_URL=http://127.0.0.1:8080/v1`. Do not assume every GGUF is a BitNet model or that a model name proves the model has loaded.

## Runtime checks

- `GET /api/providers/status`: safe configuration summary only.
- `POST /api/diagnostics/provider`: a real generation smoke test.
- Existing backend and frontend suites: regression checks for the full app.
- `python scripts/security_invariants.py`: security invariant checks.
- `python scripts/check_android_npu.py`: Android/NPU static checks.

## Operational boundary

For offline operation, use local BitNet or the original custom runner and leave web search disabled. Firecrawl requires an internet connection and a server-side API key. Hosted AI providers require internet, a key and explicit fallback consent. The ChatGPT account's connected apps are not silently shared with this app.
