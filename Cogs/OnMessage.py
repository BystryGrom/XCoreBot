import discord
from discord.ext import commands
from CogsClasses import Nrp, Ai
from time import time

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.last_airesponse = 0

        @bot.event
        async def on_message(message: discord.Message):
            await Nrp.change_money(len(message.content), message.author)
            if message.content.startswith(bot.user.mention) and message.channel == message.guild.get_channel(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Offtop"]):
                if time() - self.last_airesponse > 10:
                    response = await Ai.create_request(message.content[22:], message.author)
                    self.last_airesponse = time()
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
            await Nrp.change_money(len(before.content) - len(after.content), after.author, -1)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
    print('Cock\'s loaded')