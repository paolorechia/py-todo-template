"""Added item table new column

Revision ID: 01189eb5a866
Revises:
Create Date: 2024-08-18 14:28:23.538726

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "01189eb5a866"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("item", sa.Column("new_column", sa.String(length=30), nullable=True))


def downgrade() -> None:
    op.drop_column("item", "new_column")
