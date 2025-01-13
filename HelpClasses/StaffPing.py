import discord
from discord.ext import commands

class StaffPing:
    async def process_ping(message: discord.Message, bot_object: commands.Bot):  # АХАХХАААХ БЕГИТЕ Я КОНЧЕННЫЙ
        if message.author.id == bot_object.user.id:
            return

        staff_guild = bot_object.get_guild(int(bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["guild_id"]))
        mod_role = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Moderator"]
        helper_role = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Helper"]
        anketolog_role = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Anketolog"]
        master_role = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Master"]
        redacted_message = message.content.replace(f"<@&{mod_role}>", "Модераторы")
        redacted_message = redacted_message.replace(f"<@&{helper_role}>", "Хелперы")
        redacted_message = redacted_message.replace(f"<@&{anketolog_role}>", "Анкетологи")
        redacted_message = redacted_message.replace(f"<@&{master_role}>", "Мастера")

        if message.content.find(str(mod_role)) != -1:
            channel = staff_guild.get_channel(bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Channels"]["ModeratorPing"])
            roleid = bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Roles"]["ModeratorPing"]
            role = channel.guild.get_role(roleid)
            await channel.send(f"{role.mention} {message.jump_url}" + "\n" + redacted_message)

        if message.content.find(str(helper_role)) != -1:
            channel = staff_guild.get_channel(bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Channels"]["HelperPing"])
            roleid = bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Roles"]["HelperPing"]
            role = channel.guild.get_role(roleid)
            await channel.send(f"{role.mention} {message.jump_url}" + "\n" + redacted_message)

        if message.content.find(str(anketolog_role)) != -1:
            channel = staff_guild.get_channel(bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Channels"]["AnketologPing"])
            roleid = bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Roles"]["AnketologPing"]
            role = channel.guild.get_role(roleid)
            await channel.send(f"{role.mention} {message.jump_url}" + "\n" + redacted_message)

        if message.content.find(str(master_role)) != -1:
            channel = staff_guild.get_channel(bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Channels"]["MasterPing"])
            roleid = bot_object.SETTINGS["Guilds"]["DEV_GUILD"]["Roles"]["MasterPing"]
            role = channel.guild.get_role(roleid)
            await channel.send(f"{role.mention} {message.jump_url}" + "\n" + redacted_message)