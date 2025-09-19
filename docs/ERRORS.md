# Error Model

- 400 `validation_error`
- 401 `unauthorized`
- 403 `missing scope`
- 413 `payload too large`
- 415 `unsupported media type`
- 429 `rate limited` or `monthly quota exceeded`
- 500 `internal_error`
Each error returns JSON with `detail` and a unique `X-Request-ID` header for support.
