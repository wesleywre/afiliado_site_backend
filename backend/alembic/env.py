from logging.config import fileConfig

from alembic import context

# Importar a Base do arquivo de modelos
from app.database import Base
from app.models.comment import Comment
from app.models.coupon import Coupon
from app.models.like import Like
from app.models.permission import Permission
from app.models.promotion import Promotion
from app.models.role import Role
from app.models.user import User
from app.models.view import View
from sqlalchemy import engine_from_config, pool

# Configuração de logging do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define a metadata dos modelos para o Alembic detectar automaticamente
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
