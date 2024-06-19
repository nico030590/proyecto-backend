"""Initial migration.

Revision ID: ef999559fc04
Revises: 
Create Date: 2024-06-17 20:11:09.271112

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef999559fc04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('aclamadas')
    op.drop_table('administradores')
    op.drop_table('peliculas')
    op.drop_table('busquedas')
    op.drop_table('tendencias')
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('pais',
               existing_type=mysql.VARCHAR(length=2),
               nullable=False)
        batch_op.alter_column('fecha_registro',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('fecha_registro',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('pais',
               existing_type=mysql.VARCHAR(length=2),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    op.create_table('tendencias',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('pelicula_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fecha', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['pelicula_id'], ['peliculas.id'], name='tendencias_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('busquedas',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('termino', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('fecha', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], name='busquedas_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('peliculas',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('titulo', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('descripcion', mysql.TEXT(), nullable=True),
    sa.Column('año', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genero', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('director', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('actores', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('imagen_url', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('trailer_url', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('fecha_agregado', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('administradores',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], name='administradores_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('aclamadas',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('pelicula_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fecha', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['pelicula_id'], ['peliculas.id'], name='aclamadas_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
