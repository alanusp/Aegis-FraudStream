# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

from .config import settings
def verify_auth(header, api_key_header):
    if settings.api_key and api_key_header==settings.api_key:
        return True
    if not (settings.jwt_secret or settings.jwks_url):
        return True if not settings.api_key else False
    if not header:
        return False
    try:
        parts=header.split()
        if len(parts)!=2 or parts[0].lower()!='bearer':
            return False
        token=parts[1]
        aud = settings.jwt_audience
        iss = settings.jwt_issuer
        if settings.jwt_secret:
            import jwt
            jwt.decode(token, settings.jwt_secret, algorithms=['HS256'], audience=aud, issuer=iss, options={"verify_aud": bool(aud), "verify_iss": bool(iss)})
            return True
        if settings.jwks_url:
            import jwt
            from jwt import PyJWKClient
            jwk_client = PyJWKClient(settings.jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token)
            jwt.decode(token, signing_key.key, algorithms=['RS256'], audience=aud, issuer=iss, options={"verify_aud": bool(aud), "verify_iss": bool(iss)})
            return True
    except Exception:
        return False
    return False

def verify_jwt(request: Request) -> None:
    if not settings.jwt_hs256_secret:
        return
    authz = request.headers.get("authorization") or request.headers.get("Authorization")
    if not authz or not authz.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authz.split(" ",1)[1]
    try:
        import jwt  # PyJWT
        jwt.decode(token, settings.jwt_hs256_secret, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="invalid bearer token")

_JWKS_CACHE: dict | None = None
_JWKS_TS: float | None = None

def _load_jwks(url: str) -> dict:
    global _JWKS_CACHE, _JWKS_TS
    import time, json, urllib.request
    if _JWKS_CACHE and _JWKS_TS and time.time() - _JWKS_TS < 300:
        return _JWKS_CACHE
    with urllib.request.urlopen(url, timeout=5) as r:
        data = json.loads(r.read().decode())
    _JWKS_CACHE, _JWKS_TS = data, time.time()
    return data

def verify_oidc_jwt(request: Request) -> None:
    if not settings.oidc_jwks_url:
        return
    authz = request.headers.get("authorization") or request.headers.get("Authorization")
    if not authz or not authz.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authz.split(" ",1)[1]
    try:
        import jwt
        from jwt.algorithms import RSAAlgorithm  # type: ignore
        jwks = _load_jwks(settings.oidc_jwks_url)
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        key = None
        for k in jwks.get("keys", []):
            if k.get("kid")==kid:
                key = RSAAlgorithm.from_jwk(json.dumps(k))
                break
        jwt.decode(token, key=key, algorithms=["RS256"], audience=settings.oidc_audience if settings.oidc_audience else None, options={"verify_aud": bool(settings.oidc_audience)}, issuer=settings.oidc_issuer if settings.oidc_issuer else None, leeway=5)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid bearer token")

def require_scope(request: Request, needed: str) -> None:
    scopes = getattr(getattr(request, "state", object()), "api_scopes", "") or ""
    if not scopes:
        return  # allow anonymous if no API key present
    parts = {p.strip() for p in scopes.split(",") if p.strip()}
    if needed not in parts and "*" not in parts:
        raise HTTPException(status_code=403, detail=f"missing scope: {needed}")
