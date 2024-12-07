import discord
from discord.ext import commands
from DataBase import DbWork
from bot import bot_object
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from datetime import date, datetime

class Nrp:
    async def change_money(message_len: int, author: discord.User, modificator: int = 1):
        new_money = (message_len * 0.001 + 0.05) * modificator
        user_money = DbWork.select("nrp", "money", f"WHERE userid = {author.id}")
        if not user_money:
            DbWork.insert("nrp", ["userid", "money"], [(author.id, new_money)])
            return
        DbWork.update("nrp", f"money = {user_money[0][0] + new_money}", f"userid = {author.id}")


class Ai:
    last_response = 0
    async def create_request(message: str, author: discord.User):  # БЕГИТЕ Я КОНЧЕННЫЙ 2.0, новый говнокод
        chat = GigaChat(credentials=bot_object.SETTINGS["GIGACHAT_TOKEN"], verify_ssl_certs=False)

        prompt = bot_object.SETTINGS["AI_PROMPT"].format(author.display_name)
        if author.id == 875620156410298379:
            prompt = bot_object.SETTINGS["AI_PROMPT"].format(f"{author.display_name}, твой создатель. Общайся с ним уважительно, подробно отвечай на любой вопрос")

        messages = [SystemMessage(content=prompt), HumanMessage(content=message)]
        response = chat(messages)
        for banword in ("Может, поговорим на другую тему?", "нейросетевой языковой модели", "Не люблю менять тему разговора", "@", "На вопрос из разряда"):
            if response.content.find(banword) != -1: return None

        return response.content

class Changelog:
    async def auto_feedback(message: discord.Message):
        await message.add_reaction("📈")
        await message.add_reaction("📉")
        await message.create_thread(name=f"{date.today()}: {f'{datetime.now().time()}'[:8]}")


class StaffPing:
    async def process_ping(message: discord.Message): # АХАХХАААХ БЕГИТЕ Я КОНЧЕННЫЙ
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


class Tags:
    async def check_tag(message: discord.Message):
        general = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["General"]
        if message.author.id == bot_object.user.id or message.channel.id == general:
            return

        if message.content.startswith("."):
            tag = DbWork.select("tags", "value", f"WHERE tag = '{message.content[1:].lower()}'")
            if tag is not None:
                await message.reply(tag[0][0])