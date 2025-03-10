"""correcao

Revision ID: dc004624f45e
Revises: 9155331392fe
Create Date: 2025-02-26 21:12:16.507784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc004624f45e'
down_revision: Union[str, None] = '9155331392fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('sensor_data_server_ulid_fkey', 'sensor_data', type_='foreignkey')
    op.create_foreign_key(None, 'sensor_data', 'server', ['server_ulid'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sensor_data', type_='foreignkey')
    op.create_foreign_key('sensor_data_server_ulid_fkey', 'sensor_data', 'sensor_data', ['server_ulid'], ['id'])
    # ### end Alembic commands ###
