import os
from collections.abc import Generator

from sqlalchemy import JSON, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgres://", "postgresql+psycopg://", 1)
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) if engine else None


class Base(DeclarativeBase):
    pass


class SupportCase(Base):
    __tablename__ = "support_cases"

    id = mapped_column(String(36), primary_key=True)
    created_at = mapped_column(DateTime(timezone=True), nullable=False)
    status = mapped_column(String(32), default="triaged")
    review_status = mapped_column(String(32), nullable=True)
    network = mapped_column(String(32))
    wallet_address = mapped_column(String(128), nullable=True)
    transaction_hash = mapped_column(String(128), nullable=True)
    contract_address = mapped_column(String(128), nullable=True)
    error_message = mapped_column(Text)
    tool_used = mapped_column(String(64))
    issue_category = mapped_column(String(64), nullable=True)
    triage = mapped_column(JSON, default=dict)
    response = mapped_column(Text, nullable=True)


def get_session() -> Generator[Session, None, None]:
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL is not configured")
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    if engine:
        Base.metadata.create_all(engine)


def case_to_dict(case: SupportCase) -> dict:
    return {column.name: getattr(case, column.name) for column in SupportCase.__table__.columns}