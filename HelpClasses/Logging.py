import discord
from discord.ext import commands

class Logging:
    def __int__(self, bot_object: commands.Bot):
        super().__int__()
        self.bot = bot_object

    async def warn(self, user: discord.Member, target: discord.Member, grade: int, reason: str):
        mod_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["ModerationLogs"]
        channel = self.bot.get_channel(mod_log)
        await channel.send(f"# Warn\n### Staff: {user.mention}\n- User: {target.mention}:\n- Grade: {grade}\n- Reason: {reason}")

    async def delete_warn(self, user: discord.Member, target: discord.Member, grade: int, reason: str):
        mod_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["ModerationLogs"]
        channel = self.bot.get_channel(mod_log)
        await channel.send(f"# Delete Warn\n### Staff: {user.mention}\n- User: {target.mention}:\n- Grade: {grade}\n- Reason: {reason}")

    async def ban(self, user: discord.Member):
        mod_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["ModerationLogs"]
        channel = self.bot.get_channel(mod_log)
        await channel.send(f"# Ban\n- User: {user.mention}")

    async def addCurrency(self, user: discord.Member, target: discord.Member,amount: int, currency: str):
        rp_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpLogs"]
        channel = self.bot.get_channel(rp_log)
        await channel.send(f"# Add Currency\n### Staff: {user.mention}\n- User: {target.mention}\n- Currency: {currency}\n- Amount: {amount}")

    async def giveCurrency(self, user: discord.Member, target: discord.Member, amount: int, currency: str):
        rp_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpLogs"]
        channel = self.bot.get_channel(rp_log)
        await channel.send(f"# Give Currency\n- {user.mention} -> {target.mention}\n- Currency: {currency}\n- Amount: {amount}")

    async def addItem(self, user: discord.Member, target: discord.Member,name: str, desc: str, amount: int):
        rp_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpLogs"]
        channel = self.bot.get_channel(rp_log)
        await channel.send(f"# Add Item\n### Staff: {user.mention}\n- User: {target.mention}\n- Name: {name}\n- Description: {desc}\n- Amount: {amount}")

    async def giveItem(self, user: discord.Member, target: discord.Member, name: str, amount: int):
        rp_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RpLogs"]
        channel = self.bot.get_channel(rp_log)
        await channel.send(f"# Give Item\n- {user.mention} -> {target.mention}\n- Name: {name}\n- Amount: {amount}")

    async def registration(self, user: discord.Member, target: discord.Member, name: str, au: str):
        characters_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["CharacterLogs"]
        channel = self.bot.get_channel(characters_log)
        await channel.send(f"# Registration\n### Staff: {user.mention}\n- User: {target.mention}\n- {name} from {au}")
    async def exitRp(self, name: str, user: discord.Member, target: discord.Member):
        characters_log = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["CharacterLogs"]
        channel = self.bot.get_channel(characters_log)
        await channel.send(f"# Exit RP\n- {user.mention} -> {target.mention}\n- Name: {name}")