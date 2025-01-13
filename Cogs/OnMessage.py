from HelpClasses.StaffPing import *
from HelpClasses.Tags import *
from HelpClasses.AI import *
from HelpClasses.NonRP import *
from HelpClasses.QWE import *
from HelpClasses.Changelog import *
from discord.ext import commands
import discord

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        @bot.event
        async def on_message(message: discord.Message):
            member = message.guild.get_member(message.author.id)
            await StaffPing.process_ping(message, bot)
            await Tags.check_tag(message, bot)

            await Qwe.qwe_request(self.bot, message, message.author)
            await Ai().create_request(self.bot, message, message.author)

            if type(message.channel) is not discord.DMChannel:
                try: await Nrp.change_money(len(message.content), member)
                except: print(message.content)

            if message.channel.id == bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpProfile"]:
                await message.create_thread(name=f"Проверка {message.author.name}")
                on_checking = message.guild.get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["OnCheking"])
                await message.author.add_roles(on_checking)

            if message.channel.id == bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Changelog"]:
                await Changelog.auto_feedback(message)

        @bot.event
        async def on_message_delete(message: discord.Message):
            member = message.guild.get_member(message.author.id)
            if not (type(message.channel) is discord.DMChannel):
                await Nrp.change_money(len(message.content), member, -1)

        @bot.event
        async def on_message_edit(before: discord.Message, after: discord.Message):
            member = after.guild.get_member(after.author.id)
            if not (type(after.channel) is discord.DMChannel):
                await Nrp.change_money(len(before.content) - len(after.content), member, -1)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
    print('Cock\'s loaded')