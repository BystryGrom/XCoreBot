import discord
from discord.ext import commands
from CogsClasses import *
from time import time

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.last_airesponse = 0

        @bot.event
        async def on_message(message: discord.Message): # АХАХАХАХАХАХ БЕГИТЕ Я КОНЧЕННЫЙ ХАХАХАХАХ
            await StaffPing.process_ping(message, bot)
            await Tags.check_tag(message, bot)
            
            if message.content.startswith("qwe"):
                if message.guild.id == 1230202913901772980:
                    await message.delete()
                    await message.channel.send(message.content[3:])
                    print(1)
                else:
                    
                    role = message.guild.get_role(1301509538700197949)
                    if role in message.author.roles:
                        await message.delete()
                        await message.channel.send(message.content[3:])
            if not (type(message.channel) is discord.DMChannel):
                await Nrp.change_money(len(message.content), message.author)
            if message.content.startswith(bot.user.mention) and message.channel == message.guild.get_channel(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Offtop"]):
                if time() - self.last_airesponse > 15:
                    response = await Ai.create_request(message.content[22:], message.author)
                    self.last_airesponse = time()
                    if response is None:
                        await message.add_reaction("❌")
                    else:
                        if len(response) > 2000:
                            await message.reply(response[:(len(response) // 2)])
                            await message.channel.send(response[(len(response) // 2):])
                        else: await message.reply(response)

            if message.channel.id == bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpProfile"] or message.channel.id == 1321173638879248404:
                thread = await message.create_thread(name=f"Проверка {message.author.name}")


                on_cheking = message.guild.get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["OnCheking"])
                if message.channel.id != 1321173638879248404:
            
                    await message.author.add_roles(on_cheking)
            if message.channel.id == bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Changelog"]:
                await Changelog.auto_feedback(message)

        @bot.event
        async def on_message_delete(message: discord.Message):
            if not (type(message.channel) is discord.DMChannel):
                await Nrp.change_money(len(message.content), message.author, -1)

        @bot.event
        async def on_message_edit(before: discord.Message, after: discord.Message):
            if not (type(after.channel) is discord.DMChannel):
                await Nrp.change_money(len(before.content) - len(after.content), after.author, -1)


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
    print('Cock\'s loaded')