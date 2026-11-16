# OmniSearch Interstellar v4.0.0 — Connected AI and research gateway

## What changed

v4 adds a server-side OpenAI-compatible chat-completions adapter while retaining the existing local command runner. The default stays `local_command`; the app does not silently send student prompts to a hosted service. The connected route is selected only when the operator sets `OMNI_AI_PROVIDER=openai_compatible`.

The connected adapter accepts the safe teaching envelope already used by OmniSearch: answer, title, scene, declarative animation, diagram, mathematical plot, knowledge check and sources. Model-created URLs are never trusted as citations. When Firecrawl retrieval is configured, only URLs returned by that retrieval step are exposed as source cards.

## Microsoft BitNet local server

The official Microsoft BitNet project provides `bitnet.cpp`, an inference runtime for supported BitNet b1.58 checkpoints. Its upstream `run_inference_server.py` starts `llama-server`, which provides an OpenAI-compatible chat-completions endpoint.

- https://github.com/microsoft/BitNet
- https://huggingface.co/microsoft/BitNet-b1.58-2B-4T-gguf
- https://arxiv.org/abs/2502.11880

Build and prepare the upstream runtime using its current instructions. A typical server launch from the BitNet checkout is:

```bash
python run_inference_server.py \
  --model /absolute/path/to/ggml-model-i2_s.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --threads 4 \
  --ctx-size 4096
```

The exact model filename, thread count and context size depend on the downloaded release and available RAM. Do not expose this server on `0.0.0.0` without an authenticated reverse proxy and network policy.

Set the OmniSearch backend environment:

```dotenv
OMNI_AI_PROVIDER=openai_compatible
OMNI_OPENAI_BASE_URL=http://127.0.0.1:8080/v1
OMNI_OPENAI_MODEL=bitnet
OMNI_OPENAI_API_KEY=
```

Restart FastAPI and inspect `GET /api/providers/status`. Run `POST /api/diagnostics/provider` to make an actual short generation probe. A configured URL alone is not proof that a model loaded successfully.

## Hosted OpenAI-compatible provider (optional)

Set an official HTTPS base URL, model identifier and key on the backend host only:

```dotenv
OMNI_AI_PROVIDER=openai_compatible
OMNI_OPENAI_BASE_URL=https://provider.example/v1
OMNI_OPENAI_MODEL=your-model-id
OMNI_OPENAI_API_KEY=your-server-side-secret
```

This is a generic OpenAI-compatible protocol adapter; it does not imply that all providers support the same model names, context limits, JSON behaviour or rate limits. Confirm those details with the provider.

Remote endpoints must use HTTPS and a key. Plain HTTP is accepted only for loopback addresses. Provider URLs are environment-controlled, not supplied by browser requests. Never put API keys in frontend assets, Android resources, browser storage, public repositories or chat messages.

## Explicit local-first fallback

Keep `OMNI_AI_PROVIDER=local_command` to use the existing BitCOS/custom command runner as the primary brain. A remote fallback is allowed only when both flags are set:

```dotenv
OMNI_AI_FALLBACK=openai_compatible
OMNI_REMOTE_FALLBACK_CONSENT=true
```

This is a privacy boundary: when enabled, the learner's question and bounded learning context can be sent to the remote endpoint. Leave it disabled unless an appropriate user disclosure and consent flow exists.

## Firecrawl research connector

Live retrieval is optional and runs only on the backend. Set `OMNI_FIRECRAWL_API_KEY` to enable it. When “Use AI web search” is checked, the backend sends the question to Firecrawl Search and passes bounded excerpts to the model as untrusted reference material. Source cards are built only from URLs actually returned by Firecrawl. If the key is missing or search fails, no source cards are fabricated and the model is told that verified live results were not retrieved.

The integrated endpoint is `POST https://api.firecrawl.dev/v2/search`. See https://docs.firecrawl.dev/features/search.

## BitNet, BitCOS and the distinction

- **BitNet b1.58** is a real ternary-weight LLM family; Microsoft's `bitnet.cpp` is an inference runtime for supported checkpoints.
- **I2_S** is an upstream packing/quantization option. Do not assume that a GGUF file is literally stored at exactly 1.58 bits per parameter.
- **BitCOS** is mentioned in the original v3.9.0 source as a user-supplied custom runner/checkpoint label. That source does not define a standard BitCOS architecture, file format, tokenizer, conversion process or public runtime API. OmniSearch preserves it as a custom-command integration instead of claiming compatibility with an undefined format.
- BitNet and a BitCOS checkpoint are not interchangeable. Renaming a file does not convert model weights. Future BitCOS support needs a documented specification, validated converter, model metadata and runtime tests.

## ChatGPT plugin connections

ChatGPT's connected apps/plugins are not automatically callable from a separate Android/PWA application. They are account-scoped tools inside ChatGPT. OmniSearch must integrate external services using their published APIs and separately stored backend credentials. v4 directly implements Firecrawl Search because it has a documented HTTP API. A browser automation connector such as TinyFish needs its own supported developer API and dedicated backend adapter; do not embed a ChatGPT connector token or scrape a logged-in ChatGPT session.

## Security and limitations

- Credentials are read from backend environment variables and never returned by status endpoints.
- Remote endpoints require HTTPS; plain HTTP is allowed only on loopback.
- Browser input cannot choose an arbitrary provider URL.
- Search content is treated as untrusted data and cannot issue tool instructions.
- There is no built-in user authentication or remote-access authorization layer in this release. Keep production binds loopback-only unless a separately reviewed authenticated deployment layer is added.
- No model weights are bundled. Download a model whose licence and hardware requirements are suitable.
- The adapter supports standard non-streaming `/chat/completions` responses, not every vendor's proprietary API.
