import logging

import discord
from discord.ext import commands

from constants import TOKEN
from utils.ops_log import send_exception_log
from utils.ops_log import send_startup_log


EXTENSIONS = (
    'coin',
)


def build_intents() -> discord.Intents:
    intents = discord.Intents.none()
    intents.guilds = True
    return intents


class CoinFlipBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned,
            help_command=None,
            intents=build_intents(),
        )
        self._startup_event_sent = False

    async def setup_hook(self) -> None:
        try:
            for extension in EXTENSIONS:
                await self.load_extension(f'extensions.{extension}')
            await self.tree.sync()
        except Exception as error:
            await send_exception_log(
                event_type='config_error',
                title='Coin flip bot setup failed',
                error_value=error,
            )
            raise
        self.tree.on_error = self.on_app_command_error

    async def on_ready(self) -> None:
        if self._startup_event_sent:
            return

        self._startup_event_sent = True
        await send_startup_log(self.user, len(self.guilds))

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ) -> None:
        await send_exception_log(
            event_type='command_error',
            title='Coin flip command failed',
            error_value=error,
            actor=str(interaction.user.id) if interaction.user else None,
            safe_details={
                'command': interaction.command.name if interaction.command else 'unknown',
                'guildId': interaction.guild_id,
                'channelId': interaction.channel_id,
            },
        )

        message = 'コイン投げコマンドの実行中にエラーが発生しました。時間をおいて再試行してください。'
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    )
    CoinFlipBot().run(TOKEN)


if __name__ == '__main__':
    main()
