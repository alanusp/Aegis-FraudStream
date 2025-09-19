# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("aegis-fraudstream")
except PackageNotFoundError:
    # Fallback during editable installs or when metadata is unavailable
    __version__ = "0.0.0"

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

__all__=['__version__']
# PRESERVED ORIGINAL VERSION: __version__='1.3.0'
