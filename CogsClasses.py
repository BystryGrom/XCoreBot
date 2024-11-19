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


async def setup(bot):
    pass
