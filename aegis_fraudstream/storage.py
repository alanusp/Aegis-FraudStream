# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from typing import Any, Optional

try:
    from sqlalchemy import create_engine, Column, Integer, Float, String, JSON, DateTime, text
    from sqlalchemy.orm import declarative_base, sessionmaker
except Exception:  # pragma: no cover
    create_engine = None  # type: ignore
    Column = Integer = Float = String = JSON = DateTime = text = None  # type: ignore
    def declarative_base():  # type: ignore
        class _B: pass
        return _B

Base = declarative_base()

class DecisionLog(Base):  # type: ignore
    __tablename__ = "decision_logs"
    id = Column  # type: ignore

_engine = None
_Session = None

def init_db(url: Optional[str]) -> None:
    global _engine, _Session
    if not url or create_engine is None:
        _engine, _Session = None, None
        return
    _engine = create_engine(url, future=True)  # type: ignore
    _Session = sessionmaker(bind=_engine)  # type: ignore
