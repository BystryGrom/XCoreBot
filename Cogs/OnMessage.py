import discord
from discord.ext import commands
from bot import SETTINGS
from CoreClasses import Nrp, Ai

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        @bot.event
        async def on_message(message: discord.Message):
            await Nrp.change_money(len(message.content), message.author)
            if message.content.startswith(bot.user.mention) and message.channel == message.guild.get_channel(SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Offtop"]):
                response = await Ai.create_request(message.content[22:], message.author)
                if response is None:
                    await message.add_reaction("❌")
                else:
                    if len(response) > 2000:
                        await message.reply(response[:(len(response) // 2)])
                        await message.channel.send(response[(len(response) // 2):])
                    else: await message.reply(response)

        @bot.event
        async def on_message_delete(message: discord.Message):
            await Nrp.change_money(len(message.content), message.author, -1)

        @bot.event
        async def on_message_edit(before: discord.Message, after: discord.Message):
            await Nrp.change_money(len(after.content) - len(before.content), after.author)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
    print('Cock\'s loaded')