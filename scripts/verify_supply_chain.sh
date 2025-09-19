# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
IMAGE="${1:-ghcr.io/ORG/REPO:latest}"
echo "Verifying signatures and attestations for $IMAGE"
cosign verify "$IMAGE"
cosign verify-attestation "$IMAGE" --type cyclonedx
