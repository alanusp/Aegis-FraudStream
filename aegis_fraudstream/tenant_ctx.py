# SPDX-License-Identifier: Apache-2.0
import contextvars
current_tenant: contextvars.ContextVar[str] = contextvars.ContextVar("current_tenant", default="public")
