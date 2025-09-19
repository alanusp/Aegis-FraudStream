# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

#!/usr/bin/env bash
set -euo pipefail
pip install cyclonedx-bom
cyclonedx-py -e -o sbom-python.json
