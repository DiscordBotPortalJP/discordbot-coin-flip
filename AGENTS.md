# リポジトリ作業ガイド

## 対象範囲

このリポジトリは、日本語で動く単機能 Discord Bot です。機能はコイン投げに限定します。
関係のないゲーム、ダイス、ランダム選択、モデレーション、メッセージ自動化は追加せず、別の Bot リポジトリを作成または利用してください。

## ユーザー体験のルール

- Discord 上でユーザーに見えるメッセージは日本語にする。
- message listener より slash command を優先する。
- Message Content Intent を要求しない。
- 権限とセットアップ手順は最小限にする。

## 実装ルール

- Discord intents は最小限にする。この Bot は `guilds` だけを要求する。
- `DISCORD_BOT_TOKEN` や `OPS_LOG_HUB_KEY` などの secret をログ出力しない。
- 個別の incident 調査で追加 telemetry が必要な場合を除き、ops-log event は起動と例外に限定する。
- Railway 用ファイル（`Procfile`、`runtime.txt`、`mise.toml`）は標準の DiscordBotJP single-function bot policy と同期する。

## 検証

Pull Request を開く前に実行します。

```bash
python -m compileall main.py constants extensions utils
python -m flake8 main.py constants extensions utils
```
