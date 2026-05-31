# discordbot-coin-flip

日本語でコイン投げをする単機能 Discord Bot です。

## 機能

- `/coin` で表か裏をランダムに返します。
- `count` を指定すると 1 から 10 回までまとめて投げられます。
- Message Content Intent は不要です。

## 必要な権限

Discord Developer Portal で Bot を作成し、招待 URL には以下の scope を付けます。

- `bot`
- `applications.commands`

Privileged Gateway Intents は有効化しません。

## 環境変数

| 変数 | 必須 | 説明 |
| --- | --- | --- |
| `DISCORD_BOT_TOKEN` | Yes | Discord Bot token |
| `OPS_LOG_HUB_URL` | No | ops-log-hub ingest URL |
| `OPS_LOG_HUB_KEY` | No | ops-log-hub ingest key |
| `OPS_LOG_PROJECT` | No | 既定値: `discordbot-coin-flip` |
| `OPS_LOG_ENVIRONMENT` | No | 既定値: `production` |

## ローカル実行

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Railway

Railway では `Procfile` の `web: python main.py` を起動します。

設定する環境変数:

- `DISCORD_BOT_TOKEN`
- `OPS_LOG_HUB_URL`
- `OPS_LOG_HUB_KEY`
- `OPS_LOG_PROJECT=discordbot-coin-flip`
- `OPS_LOG_ENVIRONMENT=production`

## 開発

```bash
python -m compileall main.py constants extensions utils
python -m flake8 main.py constants extensions utils
```
