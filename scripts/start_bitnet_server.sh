#!/usr/bin/env bash
set -euo pipefail

# Run from a Microsoft BitNet checkout after building llama-server.
: "${BITNET_MODEL:?Set BITNET_MODEL to the absolute path of a compatible BitNet GGUF model}"
BITNET_SERVER_BIN="${BITNET_SERVER_BIN:-./build/bin/llama-server}"
BITNET_HOST="${BITNET_HOST:-127.0.0.1}"
BITNET_PORT="${BITNET_PORT:-8080}"
BITNET_THREADS="${BITNET_THREADS:-4}"
BITNET_CTX_SIZE="${BITNET_CTX_SIZE:-4096}"

if [[ ! -x "$BITNET_SERVER_BIN" ]]; then
  echo "BitNet llama-server not found or not executable: $BITNET_SERVER_BIN" >&2
  echo "Build upstream BitNet first: https://github.com/microsoft/BitNet" >&2
  exit 2
fi

exec "$BITNET_SERVER_BIN" \
  --model "$BITNET_MODEL" \
  --host "$BITNET_HOST" \
  --port "$BITNET_PORT" \
  --threads "$BITNET_THREADS" \
  --ctx-size "$BITNET_CTX_SIZE" \
  --n-gpu-layers 0
