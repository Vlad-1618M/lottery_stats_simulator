#!/bin/bash

set -e

GO_VERSION=1.24.0
echo "[INFO]: Installing Go $GO_VERSION..."

# ... get/install dependencies:
apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates

# ... download/unpack Go setup:
curl -LO https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
rm -rf /usr/local/go
tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz
rm go${GO_VERSION}.linux-amd64.tar.gz

# ... configure/add to PATH | current shell sesison only:
export PATH="/usr/local/go/bin:$PATH"

# ... confirm installation:
go version
