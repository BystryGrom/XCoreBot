import discord
from discord.ext import commands

from DataBase import DbWork
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from json import load

with open("Resources/CONFIG.json", "r") as file:
    SETTINGS = load(file)

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
        chat = GigaChat(credentials=SETTINGS["GIGACHAT_TOKEN"], verify_ssl_certs=False)

        prompt = SETTINGS["AI_PROMPT"].format(author.display_name)
        if author.id == 875620156410298379:
            prompt = SETTINGS["AI_PROMPT"].format(
                f"{author.display_name}, твой создатель. Общайся с ним уважительно, подробно отвечай на любой вопрос")

        messages = [SystemMessage(content=prompt), HumanMessage(content=message)]
        response = chat(messages)
        for banword in (
        "Может, поговорим на другую тему?", "нейросетевой языковой модели", "Не люблю менять тему разговора", "@",
        "На вопрос из разряда"):
            if response.content.find(banword) != -1: return None

        return response.content


class Changelog:
    async def auto_feedback(message: discord.Message):
        await message.add_reaction("📈")
        await message.add_reaction("📉")
        await message.create_thread(name=f"{datetime.date().today()}: {f'{datetime.now().time()}'[:8]}")


class StaffPing:
    async def process_ping(message: discord.Message, bot_object: commands.Bot):  # АХАХХАААХ БЕГИТЕ Я КОНЧЕННЫЙ
        if message.author.id == bot_object.user.id:
            return

        staff_guild = bot_object.get_guild(int(SETTINGS["Guilds"]["DEV_GUILD"]["guild_id"]))
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
    async def check_tag(message: discord.Message, bot_object: commands.Bot):
        general = bot_object.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["General"]
        if message.author.id == bot_object.user.id:# or message.channel.id == general:
            return

        if message.content.startswith("."):
            tag = DbWork.select("tags", "value", f"WHERE tag = '{message.content[1:].lower()}'")

            if tag:
                await message.reply(tag[0][0])


class Banner:
    async def change_banner(bot: commands.Bot):
        main_guild = bot.get_guild(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"])
        users_count = main_guild.member_count
        voice_users = 0
        for voice in main_guild.voice_channels:
            for member in voice.members:
                voice_users += 1

        general = main_guild.get_channel(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["General"])
        now = datetime.now()
        if now != 0:
            now = now.replace(hour=now.hour - 1)
        activities = []
        async for message in general.history(after=now):
            activities.append(message.author.id)
        unique_users = set(activities)
        best = (0, 0)
        for user in unique_users:
            if activities.count(user) > best[1]:
                best = (user, activities.count(user))

        best_user = bot.get_user(best[0])

        banner = Image.open("Resources/banner.png").convert("RGBA")
        await best_user.avatar.save("Resources/avatar.png")
        big_avatar = Image.open("Resources/avatar.png").convert("RGBA")
        mask = Image.open("Resources/mask.png").convert("RGBA").resize((250, 250))
        small_avatar = big_avatar.resize((250, 250))
        username = best_user.name
        new_banner = banner.copy()
        draw = ImageDraw.Draw(new_banner)
        font = ImageFont.truetype("Resources/Alphatermination.ttf", 150)
        draw.text((225, 425), str(users_count), (255, 255, 255), font=font)
        if voice_users < 10:
            draw.text((225, 585), str(voice_users), (255, 255, 255), font=font)
        else:
            draw.text((195, 585), str(voice_users), (255, 255, 255), font=font)
        user_font = ImageFont.truetype("Resources/Alphatermination.ttf", 250 - (len(username) * 7.4))
        draw.text((350, 950 + len(username) * 4), username, (255, 255, 255), font=user_font)
        new_banner.paste(small_avatar, (60, 950), mask)
        new_banner.save("./new_banner.gif")
        with open("./new_banner.gif", "rb") as file:
            await main_guild.edit(banner=file.read())


class StaffStatistic:
    async def ankets(bot: commands.Bot):
        ankets = DbWork.select("characters", "anketolog")

        amount = {}
        for anket in ankets:
            if amount.get(anket[0]) is None:
                amount[anket[0]] = 1
                continue
            new_amount = amount.get(anket[0]) + 1
            amount[anket[0]] = new_amount
        amount = sorted(amount.items(), key=lambda item: item[1])
        amount.reverse()
        amount = dict(amount)

        result = ""
        for id in amount.keys():
            if bot.get_user(id) is None: continue
            result += f"### `{bot.get_user(id).name}` - {amount.get(id)} анкет\n"

        result_embed = discord.Embed(description=result, colour=bot.SETTINGS["MAIN_COLOR"])
        channel = bot.get_channel(1316051926982332436)
        async for message in channel.history(limit=10000):
            await message.delete()
        await channel.send(embed = result_embed)
