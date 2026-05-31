# Repository Guidelines

## Project Scope

This repository is a single-function Japanese Discord Bot. Keep the bot focused on
coin flips only. Do not add unrelated games, dice, random choice, moderation, or
message automation features here; create or use another bot repository instead.

## UX Rules

- User-facing Discord messages must be Japanese.
- Prefer slash commands over message listeners.
- Do not require Message Content Intent.
- Keep permissions and setup steps minimal.

## Engineering Rules

- Use minimal Discord intents. This bot should only require `guilds`.
- Never log or print secrets such as `DISCORD_BOT_TOKEN` or `OPS_LOG_HUB_KEY`.
- Send ops-log events for startup and exceptions only unless a specific incident
  review requires more telemetry.
- Keep Railway deployment files (`Procfile`, `runtime.txt`, `mise.toml`) in sync
  with the standard DiscordBotPortalJP Python template.

## Validation

Before opening a PR, run:

```bash
python -m compileall main.py constants extensions utils
python -m flake8 main.py constants extensions utils
```

