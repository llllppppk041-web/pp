# OmniSearch Interstellar — v4.0.0 AI Gateway Evolution

This public repository is the **v4.0.0 connected-AI evolution layer** for the original OmniSearch Interstellar v3.9.0 application.

## What this release adds

- A backend OpenAI-compatible chat-completions gateway.
- Local Microsoft BitNet `llama-server` connection support.
- Optional HTTPS hosted-provider support with backend-only credentials.
- Explicit local-first fallback controls.
- Optional Firecrawl web research with source URL verification.
- Provider status and diagnostic endpoints.
- Documentation and launch scripts for the BitNet server.

## Important scope note

This repository currently publishes the v4 integration layer and its documentation. The full original OmniSearch app contains the existing Android, PWA, animation, learning, visualisation and test modules; that complete evolved source bundle is supplied separately as `omnisearch-interstellar-v4.0.0-full-source.zip` in the conversation. This repository is not yet a complete mirror of all 225 source files.

## Start here

1. Read [AI_PROVIDER_GATEWAY.md](AI_PROVIDER_GATEWAY.md).
2. Copy `.env.example` into the backend's private `.env` file.
3. Start a local BitNet server, or configure an HTTPS OpenAI-compatible endpoint.
4. Select `OMNI_AI_PROVIDER=openai_compatible`.
5. Start the FastAPI backend and check `GET /api/providers/status`.
6. Run `POST /api/diagnostics/provider` before using the model for lessons.

## Privacy defaults

The default remains `OMNI_AI_PROVIDER=local_command`. Remote fallback is disabled unless both `OMNI_AI_FALLBACK=openai_compatible` and `OMNI_REMOTE_FALLBACK_CONSENT=true` are explicitly configured. Never commit `.env`, provider API keys or downloaded model weights.

## Validation of the complete v4.0.0 source bundle

- Backend: 269 tests passed.
- Frontend: 1,810 tests passed.
- Android/NPU static checks: 97/97 passed.
- Frontend integrity and security invariant checks passed.
- SHA-256 manifest: 226 files verified.

These tests were run against the complete v4.0.0 source bundle, not this overlay-only repository.

## BitNet and BitCOS

BitNet b1.58 with Microsoft's `bitnet.cpp` is a documented model/runtime path. BitCOS remains a custom runner/checkpoint label from the original source, not a standard model format validated by this project. The two are not interchangeable.

Upstream BitNet: https://github.com/microsoft/BitNet
