from HelpClasses.StaffPing import *
from HelpClasses.Tags import *
from HelpClasses.NonRP import *
from discord.ext import commands
import discord


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        @bot.event
        async def on_message(message: discord.Message):
            try: member = message.guild.get_member(message.author.id)
            except: pass

            await StaffPing.process_ping(message, bot)
            await Tags.check_tag(message, bot)

            if message.content.startswith("qwe"):
                role = message.guild.get_role(1301509538700197949)
                if role in message.author.roles or message.guild.id == 1230202913901772980:
                    await message.delete()
                    await message.channel.send(message.content[3:])

            if type(message.channel) is not discord.DMChannel:
                try: await Nrp.change_money(len(message.content), member)
                except: pass

            if message.channel.id == bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpProfile"] or message.channel.id == bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpProfileCringe"]:
                thread = await message.create_thread(name=f"Проверка {message.author.name}")
                on_checking = message.guild.get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["OnCheking"])
                anketolog = message.guild.get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Anketolog"])
                await thread.send(anketolog.mention)
                await message.author.add_roles(on_checking)


        @bot.event
        async def on_message_delete(message: discord.Message):
            member = message.guild.get_member(message.author.id)
            if not (type(message.channel) is discord.DMChannel):
                await Nrp.change_money(len(message.content), member, -1)

        @bot.event
        async def on_message_edit(before: discord.Message, after: discord.Message):
            member = after.guild.get_member(after.author.id)
            if not (type(after.channel) is discord.DMChannel) and member is not None:
                await Nrp.change_money(len(before.content) - len(after.content), member, -1)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
    print('Cock\'s loaded')
