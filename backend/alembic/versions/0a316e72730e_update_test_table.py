"""update test table

Revision ID: 0a316e72730e
Revises: 3649309990df
Create Date: 2026-06-22 19:50:55.766385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a316e72730e'
down_revision: Union[str, Sequence[str], None] = '3649309990df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
