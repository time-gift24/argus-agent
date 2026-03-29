"""rename web_search builtin

Revision ID: 8d1c2b7e4f90
Revises: 4a9d6f1b2c3d
Create Date: 2026-03-29 19:38:00

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8d1c2b7e4f90"
down_revision: Union[str, None] = "4a9d6f1b2c3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DELETE FROM tools
        WHERE is_builtin = 1
          AND name = 'web_search'
          AND EXISTS (
              SELECT 1
              FROM tools AS renamed
              WHERE renamed.is_builtin = 1
                AND renamed.name = 'web_search(stub)'
          )
        """
    )
    op.execute(
        """
        UPDATE tools
        SET name = 'web_search(stub)'
        WHERE is_builtin = 1 AND name = 'web_search'
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM tools
        WHERE is_builtin = 1
          AND name = 'web_search(stub)'
          AND EXISTS (
              SELECT 1
              FROM tools AS legacy
              WHERE legacy.is_builtin = 1
                AND legacy.name = 'web_search'
          )
        """
    )
    op.execute(
        """
        UPDATE tools
        SET name = 'web_search'
        WHERE is_builtin = 1 AND name = 'web_search(stub)'
        """
    )
