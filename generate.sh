#!/bin/sh
# Regenerate the grpc stubs from proto/devicehost.proto
set -e
uv run python -m grpc_tools.protoc -Iproto \
	--python_out=. --pyi_out=. --grpc_python_out=. \
	proto/devicehost.proto
