"""Add reviewer identity and measured time saved to review events."""
from alembic import op
import sqlalchemy as sa

revision = "0002_review_metadata"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("support_case_review_events_v2", sa.Column("reviewer_id", sa.String(128), nullable=False, server_default="local-reviewer"))
    op.add_column("support_case_review_events_v2", sa.Column("time_saved_minutes", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("support_case_review_events_v2", "time_saved_minutes")
    op.drop_column("support_case_review_events_v2", "reviewer_id")
