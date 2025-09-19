# SPDX-License-Identifier: Apache-2.0
import nox

@nox.session(python=["3.10","3.11"])
def tests(session):
    session.install("-e", ".[dev]")
    session.run("pytest","-q")

@nox.session
def lint(session):
    session.install("ruff","mypy","bandit","pytest")
    session.run("ruff","check","aegis_fraudstream")
    session.run("mypy")
    session.run("bandit","-q","-r","aegis_fraudstream")
