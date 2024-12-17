"""initial

Revision ID: d942e7a83fab
Revises: 
Create Date: 2024-12-18 02:50:56.983614

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = 'd942e7a83fab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('email', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('password', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('phone_number', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='public'
    )
    op.create_table('producers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('product_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('email', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('role', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('password_hash', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='public'
    )
    op.create_table('warehouses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('available_types', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('address', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('available_places', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('deliveries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_sum', sa.Float(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('delivery_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['supplier_id'], ['public.suppliers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('article', sa.Integer(), nullable=False),
    sa.Column('unit', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('product_group_id', sa.Integer(), nullable=False),
    sa.Column('producer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['producer_id'], ['public.producers.id'], ),
    sa.ForeignKeyConstraint(['product_group_id'], ['public.product_groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('shipments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('total_sum', sa.Float(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('shipment_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['public.clients.id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['public.warehouses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('storage_places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('storage_type', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('available_places', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['warehouse_id'], ['public.warehouses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('delivery_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('delivery_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['delivery_id'], ['public.deliveries.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['public.products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('movements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('from_storage_place_id', sa.Integer(), nullable=False),
    sa.Column('to_storage_place_id', sa.Integer(), nullable=False),
    sa.Column('movement_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['from_storage_place_id'], ['public.storage_places.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['public.products.id'], ),
    sa.ForeignKeyConstraint(['to_storage_place_id'], ['public.storage_places.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('products_in_warehouse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('storage_place_id', sa.Integer(), nullable=False),
    sa.Column('place_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['public.products.id'], ),
    sa.ForeignKeyConstraint(['storage_place_id'], ['public.storage_places.id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['public.warehouses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('shipment_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shipment_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['public.products.id'], ),
    sa.ForeignKeyConstraint(['shipment_id'], ['public.shipments.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shipment_details', schema='public')
    op.drop_table('products_in_warehouse', schema='public')
    op.drop_table('movements', schema='public')
    op.drop_table('delivery_details', schema='public')
    op.drop_table('storage_places', schema='public')
    op.drop_table('shipments', schema='public')
    op.drop_table('products', schema='public')
    op.drop_table('deliveries', schema='public')
    op.drop_table('warehouses', schema='public')
    op.drop_table('users', schema='public')
    op.drop_table('suppliers', schema='public')
    op.drop_table('product_groups', schema='public')
    op.drop_table('producers', schema='public')
    op.drop_table('clients', schema='public')
    # ### end Alembic commands ###
