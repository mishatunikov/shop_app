from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoSetting:
    """Django configuration data"""

    secret_key: str
    debug: bool
    db_prod: bool


@dataclass
class PostgresSetting:
    """Postgres configuration data"""

    db_user: str
    db_password: str
    db_host: str
    db_name: str
    db_port: int


@dataclass
class Config:
    """Project configration data."""

    django_settings: DjangoSetting
    db: PostgresSetting


def load_config() -> Config:
    """Load environment variables from .env file."""

    env = Env()
    env.read_env()
    return Config(
        DjangoSetting(
            secret_key=env.str('SECRET_KEY', 'SECRET_KEY'),
            db_prod=env.bool('DB_PROD'),
            debug=env.bool('DEBUG'),
        ),
        PostgresSetting(
            db_user=env.str('POSTGRES_USER', 'postgres'),
            db_password=env.str('POSTGRES_PASSWORD', ''),
            db_name=env.str('POSTGRES_DB', 'postgres'),
            db_host=env.str('DB_HOST', ''),
            db_port=env.int('DB_PORT', 5432),
        ),
    )


config: Config = load_config()
