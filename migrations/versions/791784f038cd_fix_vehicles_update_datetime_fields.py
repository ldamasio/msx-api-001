"""Fix/vehicles: Update datetime fields

Revision ID: 791784f038cd
Revises: 5a340568b5fd
Create Date: 2024-09-21 15:44:05.281785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '791784f038cd'
down_revision: Union[str, None] = '5a340568b5fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
