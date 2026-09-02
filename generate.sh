#!/bin/sh
# Regenerate the grpc stubs from pb/devicehost.proto.
# The proto lives inside the package so the generated absolute imports resolve.
set -e
uv run python -m grpc_tools.protoc -I. \
	--python_out=. --pyi_out=. --grpc_python_out=. \
	pb/devicehost.proto
