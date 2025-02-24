import discord
from discord.ext import commands
from DataBase import DbWork

class Tags:
    async def check_tag(message: discord.Message, bot_object: commands.Bot):
        if message.author.id == bot_object.user.id:
            return

        if message.content.startswith("."):
            tag = DbWork.select("tags", "value", f"WHERE tag = '{message.content[1:].lower()}'")

            if tag:
                await message.reply(tag[0][0])
