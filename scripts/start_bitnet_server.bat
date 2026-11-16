@echo off
setlocal
if "%BITNET_MODEL%"=="" (
  echo Set BITNET_MODEL to the full path of a compatible BitNet GGUF model.
  exit /b 2
)
if "%BITNET_SERVER_BIN%"=="" set BITNET_SERVER_BIN=build\bin\Release\llama-server.exe
if "%BITNET_HOST%"=="" set BITNET_HOST=127.0.0.1
if "%BITNET_PORT%"=="" set BITNET_PORT=8080
if "%BITNET_THREADS%"=="" set BITNET_THREADS=4
if "%BITNET_CTX_SIZE%"=="" set BITNET_CTX_SIZE=4096
"%BITNET_SERVER_BIN%" --model "%BITNET_MODEL%" --host "%BITNET_HOST%" --port "%BITNET_PORT%" --threads "%BITNET_THREADS%" --ctx-size "%BITNET_CTX_SIZE%" --n-gpu-layers 0
endlocal
