"""add tools table

Revision ID: add_tools_table
Revises:
Create Date: 2026-03-27 18:04:23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_tools_table'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tools',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(128), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('argus_schema', sa.JSON, nullable=False),
        sa.Column('system_prompt', sa.Text, nullable=True),
        sa.Column('turnend_prompt', sa.Text, nullable=True),
        sa.Column('is_builtin', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('tools')
