import discord
from discord.ext import commands

class Qwe:
    async def qwe_request(bot: commands.Bot, message: discord.Message, author: discord.User):
        if message.content.startswith("qwe"):
            if message.guild.id == 1230202913901772980:
                await message.delete()
                await message.channel.send(message.content[3:])
            else:
                role = message.guild.get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Staff"])
                if role in message.author.roles:
                    await message.delete()
                    await message.channel.send(message.content[3:])