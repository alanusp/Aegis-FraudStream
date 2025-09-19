# Contributing to Aegis FraudStream

Thank you for improving Aegis FraudStream. This guide defines how to propose changes, coding standards, reviews, and releases. By participating you agree to the Code of Conduct.

## TL;DR
1. Fork and create a topic branch from `main`.
2. Install dev deps and pre-commit hooks.
3. Write tests and docs; keep coverage ≥ 90%.
4. Lint, type-check, and run `make verify`.
5. Use Conventional Commits + DCO sign-off.
6. Open a PR; ensure all checks are green.

## Ways to contribute
- Report bugs, request features, or propose design changes.
- Improve docs (tutorials, examples, API references).
- Add tests, refactors, performance, and security hardening.
- Help triage issues and review pull requests.

## Communication
- Issues/PRs: GitHub tracker.
- Security: see SECURITY_CONTACTS and `.well-known/security.txt`.
- Maintainer: alanusp • alanursapu@gmail.com

## Development setup
Prerequisites: Python 3.11+, git, `uv`, Docker (optional), Helm (optional).

    git clone https://github.com/alanusp/aegis-fraudstream.git
    cd aegis-fraudstream
    python -m venv .venv && . .venv/bin/activate
    pip install -U pip uv
    uv pip install -e ".[dev]"
    pre-commit install

Run the service locally:

    uvicorn aegis_fraudstream.app:app --host 0.0.0.0 --port 8080

Full local gate:

    make verify

Optional extras:

    mkdocs serve -a 127.0.0.1:8000
    nox -s lint typecheck tests
    tox

## Coding standards
- Style: ruff (format + lint), no unused code (vulture), security checks (bandit).
- Types: mypy strict; add or refine type hints.
- Tests: pytest; keep unit tests fast and deterministic.
- Coverage: enforced at 90% via pytest `--cov-fail-under`.
- Docs: MkDocs Material; keep examples runnable.
- API: OpenAPI must match implementation; run `make openapi-all`.
- Config: Add SPDX headers and keep files REUSE-compliant.
- Accessibility: docs must pass pa11y CI.

## Commit conventions
- Use Conventional Commits:
    feat(api): add /v1/limits endpoint
    fix: correct floating point rounding in scorer
    docs: clarify Docker multi-arch steps
- Keep subject ≤ 72 chars; body explains “why” more than “how”.
- Reference issues: `Fixes #123`.
- Sign every commit with DCO:
    Signed-off-by: Your Name <alanursapu@gmail.com>
- GPG/SSH signing is recommended.

## Branching
- `main` is protected; all changes via PR.
- Use prefixes: `feat/`, `fix/`, `perf/`, `docs/`, `chore/`, `sec/`.
- Rebase on `main` before opening/merging PRs.

## Pull request checklist
- [ ] Description explains motivation and approach.
- [ ] Tests added/updated; coverage ≥ 90%.
- [ ] Lint, types, links, packaging, and docs pass locally:
    make verify
- [ ] OpenAPI updated or drift check passes.
- [ ] Helm templates render and lint:
    make helm-lint chart-test opa-k8s
- [ ] DCO sign-off present on all commits.
- [ ] No secrets or private data included.

## Testing matrix
- Unit: pytest + TestClient for API.
- Contracts: Schemathesis against ephemeral app.
- Fuzz: Atheris corpus sanity in CI.
- E2E: kind + Helm workflow deploys and exercises `/health` and `/v1/score`.
- Performance: k6 smoke with thresholds (p95 < 200 ms, error rate < 1%).
- Security: Semgrep, Bandit, ZAP baseline; IaC via Checkov/KICS; deps via OSV/Safety/pip-audit.

## Documentation
- Update user guides, examples, and references when behavior changes.
- Add new CLI or API features to README and MkDocs nav.
- Screenshots and diagrams must be reproducible from repo assets.

## Backwards compatibility
- Avoid breaking changes. If unavoidable, document migration steps, deprecate gracefully, and note in CHANGELOG.

## Licensing and ownership
- License: Apache-2.0. You certify you have rights to contribute under this license.
- Include SPDX headers in source files you add.
- Third-party code must include license notices in `THIRD_PARTY_NOTICES.md`.

## Security and privacy
- Never include secrets in code or CI.
- Follow data minimization; avoid adding PII fields by default.
- Report vulnerabilities privately (see Reporting above).

## Performance and reliability
- Add benchmarks for critical paths where applicable.
- Ensure HPA/requests/limits values remain sensible in Helm chart.
- Keep Docker images small and non-root.

## Release process (maintainers)
- Ensure `main` is green.
- Tag with SemVer; Release Drafter composes notes.
- Wheels: built by cibuildwheel on release.
- PyPI: published via Trusted Publisher OIDC.
- Container: GHCR build+push with Sigstore signing and SBOM attach.
- Docs: auto-published to GitHub Pages.

## Governance
- Decisions via RFCs and ADRs in `docs/`.
- Escalations: maintainer group; conflicts resolved with transparency.

## Thank you
Your time and expertise move Aegis FraudStream forward. Whether a typo fix or a major feature, contributions are welcome and appreciated.