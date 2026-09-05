"""Create support case and review event tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "support_cases",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=True),
        sa.Column("review_status", sa.String(32), nullable=True),
        sa.Column("network", sa.String(32), nullable=True),
        sa.Column("wallet_address", sa.String(128), nullable=True),
        sa.Column("transaction_hash", sa.String(128), nullable=True),
        sa.Column("contract_address", sa.String(128), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("tool_used", sa.String(64), nullable=True),
        sa.Column("issue_category", sa.String(64), nullable=True),
        sa.Column("triage", sa.JSON(), nullable=True),
        sa.Column("response", sa.Text(), nullable=True),
    )
    op.create_table(
        "support_case_review_events_v2",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("case_id", sa.String(36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("response", sa.Text(), nullable=True),
        sa.Column("source", sa.String(32), nullable=False, server_default="custom"),
        sa.Column("review_duration_seconds", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["case_id"], ["support_cases.id"]),
    )
    op.create_index("ix_support_case_review_events_v2_case_id", "support_case_review_events_v2", ["case_id"])


def downgrade() -> None:
    op.drop_index("ix_support_case_review_events_v2_case_id", table_name="support_case_review_events_v2")
    op.drop_table("support_case_review_events_v2")
    op.drop_table("support_cases")
