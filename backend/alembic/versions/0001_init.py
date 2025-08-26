import sqlalchemy as sa

from alembic import op

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "technicians",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=True),
    )
    op.create_index("ix_tech_id", "technicians", ["id"])
    op.create_table(
        "missions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("start", sa.DateTime(timezone=False), nullable=False),
        sa.Column("end", sa.DateTime(timezone=False), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=True),
    )
    op.create_index("ix_mission_id", "missions", ["id"])
    op.create_table(
        "availabilities",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("technician_id", sa.Integer, sa.ForeignKey("technicians.id", ondelete="CASCADE")),
        sa.Column("start", sa.DateTime(timezone=False), nullable=False),
        sa.Column("end", sa.DateTime(timezone=False), nullable=False),
        sa.Column("status", sa.Enum("available","unavailable", name="avstatus"), nullable=False, server_default="available"),
    )
    op.create_index("ix_avail_id", "availabilities", ["id"])
    op.create_index("ix_avail_tech_time", "availabilities", ["technician_id","start","end"])

def downgrade():
    op.drop_index("ix_avail_tech_time", table_name="availabilities")
    op.drop_table("availabilities")
    op.drop_index("ix_mission_id", table_name="missions")
    op.drop_table("missions")
    op.drop_index("ix_tech_id", table_name="technicians")
    op.drop_table("technicians")
    op.execute("DROP TYPE IF EXISTS avstatus")
