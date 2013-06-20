"""empty message

Revision ID: 52a791eb9a71
Revises: 2793676d8016
Create Date: 2013-06-20 00:15:37.666184

"""

# revision identifiers, used by Alembic.
revision = '52a791eb9a71'
down_revision = '2793676d8016'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('http_method', sa.String(length=250), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('resource_type', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['people.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('revisions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('resource_type', sa.String(length=250), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Enum(u'created', u'modified', u'deleted'), nullable=False),
    sa.Column('content', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table(u'versions')
    op.drop_column(u'directives', u'company')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'directives', sa.Column(u'company', mysql.TINYINT(display_width=1), nullable=False))
    op.create_table(u'versions',
    sa.Column(u'id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column(u'item_type', mysql.VARCHAR(length=250), nullable=True),
    sa.Column(u'item_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column(u'event', mysql.VARCHAR(length=250), nullable=True),
    sa.Column(u'whodunnit', mysql.VARCHAR(length=250), nullable=True),
    sa.Column(u'object', mysql.TEXT(), nullable=True),
    sa.Column(u'created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint(u'id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('revisions')
    op.drop_table('events')
    ### end Alembic commands ###