"""merge mcp and tools heads

Revision ID: 85222bba3a92
Revises: 0e07298280dd, 8d1c2b7e4f90
Create Date: 2026-03-29 20:21:32.758453

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = '85222bba3a92'
down_revision: Union[str, None] = ('0e07298280dd', '8d1c2b7e4f90')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
