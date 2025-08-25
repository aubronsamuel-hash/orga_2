from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "technicians",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
    )
    op.create_table(
        "missions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("technician_id", sa.Integer, sa.ForeignKey("technicians.id")),
        sa.Column("start", sa.DateTime),
        sa.Column("end", sa.DateTime),
    )
    op.create_table(
        "availability",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("technician_id", sa.Integer, sa.ForeignKey("technicians.id"), nullable=False),
        sa.Column("start", sa.DateTime, nullable=False),
        sa.Column("end", sa.DateTime, nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("availability")
    op.drop_table("missions")
    op.drop_table("technicians")
