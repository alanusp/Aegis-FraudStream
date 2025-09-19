# SPDX-License-Identifier: Apache-2.0
#!/bin/sh
wget -qO- http://127.0.0.1:8080/health || exit 1
