import discord
from DataBase import DbWork
from time import time

class Mute:
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.mute_role = bot.get_guild(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"]).get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Mute"])

    async def process(self, message: discord.Message):
        if self.mute_role in message.author.roles:
            mute = DbWork.select("mutes", "start, length", f"WHERE userid = {message.author.id}")[0]

            if mute[0] + mute[1] < time():
                DbWork.delete("mutes", f"userid = {message.author.id}")
                await message.author.remove_roles(self.mute_role)
                return

            await message.delete()
