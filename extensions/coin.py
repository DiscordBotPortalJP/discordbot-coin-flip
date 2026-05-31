import secrets

import discord
from discord import app_commands
from discord.ext import commands


RESULTS = ('表', '裏')


def build_result_message(outcomes: list[str]) -> str:
    if len(outcomes) == 1:
        return f'結果: **{outcomes[0]}**'

    heads = outcomes.count('表')
    tails = outcomes.count('裏')
    joined = '、'.join(outcomes)
    return f'結果: {joined}\n表: **{heads}** / 裏: **{tails}**'


class CoinCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='coin', description='コインを投げて表か裏を返します。')
    @app_commands.describe(count='投げる回数（1から10）')
    async def coin(
        self,
        interaction: discord.Interaction,
        count: app_commands.Range[int, 1, 10] = 1,
    ) -> None:
        outcomes = [secrets.choice(RESULTS) for _ in range(count)]
        await interaction.response.send_message(build_result_message(outcomes))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoinCog(bot))
