from os import getenv

from dotenv import load_dotenv

load_dotenv()


def required_env(name: str) -> str:
    value = getenv(name)
    if not value:
        raise RuntimeError(f'{name} is required')
    return value


TOKEN = required_env('DISCORD_BOT_TOKEN')

OPS_LOG_HUB_URL = getenv(
    'OPS_LOG_HUB_URL',
    'https://ops-log-hub.up.railway.app/api/ingest/discord-bot',
)
OPS_LOG_HUB_KEY = getenv('OPS_LOG_HUB_KEY')
OPS_LOG_ENVIRONMENT = getenv('OPS_LOG_ENVIRONMENT', 'production')
OPS_LOG_PROJECT = getenv('OPS_LOG_PROJECT', 'discordbot-coin-flip')
