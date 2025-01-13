import discord
from discord.ext import commands
from DataBase import DbWork

class Tags:
    async def check_tag(message: discord.Message, bot_object: commands.Bot):
        general = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["General"]
        if message.author.id == bot_object.user.id or message.channel.id == general:
            return

        if message.content.startswith("."):
            tag = DbWork.select("tags", "value", f"WHERE tag = '{message.content[1:].lower()}'")

            if tag:
                await message.reply(tag[0][0])