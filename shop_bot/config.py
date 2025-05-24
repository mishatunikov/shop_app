from dataclasses import dataclass

from environs import Env


@dataclass
class PaymentSettings:
    """Payment configuration data."""

    token: str


@dataclass
class BotSetting:
    """TG bot configuration data"""

    token: str
    redis: bool


@dataclass
class Config:
    """Project configration data."""

    bot: BotSetting
    payment: PaymentSettings


def load_config() -> Config:
    """Load environment variables from .env file."""

    env = Env()
    env.read_env()
    return Config(
        BotSetting(token=env.str('BOT_TOKEN'), redis=env.bool('REDIS')),
        PaymentSettings(token=env.str('YOOKASSA_TOKEN')),
    )
