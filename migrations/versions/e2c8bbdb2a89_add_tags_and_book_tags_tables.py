from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = 'e2c8bbdb2a89'
down_revision: Union[str, None] = 'dd19a079b08e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)

    if 'tags' not in inspector.get_table_names():
        op.create_table(
            'tags',
            sa.Column('uid', sa.Uuid(), primary_key=True, nullable=False),
            sa.Column('name', sa.VARCHAR(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        )

    if 'book_tags' not in inspector.get_table_names():
        op.create_table(
            'book_tags',
            sa.Column('book_uid', sa.Uuid(), nullable=False),
            sa.Column('tag_uid', sa.Uuid(), nullable=False),
            sa.ForeignKeyConstraint(['book_uid'], ['books.uid']),
            sa.ForeignKeyConstraint(['tag_uid'], ['tags.uid']),
            sa.PrimaryKeyConstraint('book_uid', 'tag_uid')
        )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS book_tags CASCADE;")
    op.execute("DROP TABLE IF EXISTS tags CASCADE;")
