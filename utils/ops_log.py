import asyncio
import json
import logging
import traceback
from datetime import datetime, timezone
from typing import Any
from urllib import error
from urllib import request

import discord

from constants import OPS_LOG_ENVIRONMENT
from constants import OPS_LOG_HUB_KEY
from constants import OPS_LOG_HUB_URL
from constants import OPS_LOG_PROJECT


logger = logging.getLogger(__name__)


def is_ops_log_enabled() -> bool:
    return bool(OPS_LOG_HUB_URL and OPS_LOG_HUB_KEY)


async def send_ops_log(
    *,
    event_type: str,
    severity: str,
    title: str,
    message: str | None = None,
    actor: str | None = None,
    dedupe_key: str | None = None,
    safe_details: dict[str, Any] | None = None,
) -> bool:
    if not is_ops_log_enabled():
        return False

    payload = {
        'eventType': event_type,
        'severity': severity,
        'project': OPS_LOG_PROJECT,
        'environment': OPS_LOG_ENVIRONMENT,
        'title': title,
        'message': message,
        'actor': actor,
        'dedupeKey': dedupe_key,
        'occurredAt': datetime.now(timezone.utc).isoformat(),
        'aiView': {
            'readableSummary': message or title,
            'safeDetails': safe_details or {},
        },
    }
    compact_payload = {key: value for key, value in payload.items() if value is not None}

    try:
        await asyncio.to_thread(post_event, compact_payload)
        return True
    except Exception:
        logger.exception('Failed to send event to ops-log-hub')
        return False


async def send_exception_log(
    *,
    event_type: str,
    title: str,
    error_value: BaseException,
    actor: str | None = None,
    safe_details: dict[str, Any] | None = None,
) -> bool:
    error_name = error_value.__class__.__name__
    return await send_ops_log(
        event_type=event_type,
        severity='error',
        title=title,
        message=f'{error_name}: {error_value}',
        actor=actor,
        dedupe_key=f'{OPS_LOG_PROJECT}:{event_type}:{error_name}',
        safe_details={
            **(safe_details or {}),
            'errorType': error_name,
            'errorSummary': ''.join(
                traceback.format_exception_only(type(error_value), error_value)
            ).strip(),
        },
    )


async def send_startup_log(bot_user: discord.ClientUser | None, guild_count: int) -> bool:
    return await send_ops_log(
        event_type='startup',
        severity='info',
        title='Discord Bot started',
        message='discordbot-coin-flip is ready.',
        safe_details={
            'botUser': str(bot_user),
            'guildCount': guild_count,
        },
    )


def post_event(payload: dict[str, Any]) -> None:
    if not OPS_LOG_HUB_URL or not OPS_LOG_HUB_KEY:
        return

    data = json.dumps(payload).encode('utf-8')
    req = request.Request(
        OPS_LOG_HUB_URL,
        data=data,
        method='POST',
        headers={
            'content-type': 'application/json',
            'x-log-hub-key': OPS_LOG_HUB_KEY,
        },
    )

    try:
        with request.urlopen(req, timeout=5) as response:
            response.read()
    except error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'ops-log-hub returned {exc.code}: {body}') from exc
