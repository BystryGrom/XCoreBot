import discord
from discord.ext import commands
from .CoreClasses import Nrp

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        @bot.event
        async def on_message(message: discord.Message):
            await Nrp.changeMoney(len(message.content), message.author)

        @bot.event
        async def on_message_delete(message: discord.Message):
            await Nrp.changeMoney(len(message.content), message.author, -1)

        @bot.event
        async def on_message_edit(before: discord.Message, after: discord.Message):
            await Nrp.changeMoney(len(after.content) - len(before.content), after.author)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
    print('Cock\'s loaded')