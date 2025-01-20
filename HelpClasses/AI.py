import discord
from discord.ext import commands
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat
from json import load
from time import time

active_dialogs = {}
with open("./Resources/CONFIG.json", "r") as file:
    SETTINGS = load(file)


class Ai:
    def __init__(self, bot: commands.Bot, author: discord.User):
        self.bot = bot
        self.model = GigaChat(
            credentials=SETTINGS["GIGACHAT_TOKEN"],
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            verify_ssl_certs=False,
        )
        username = author.display_name
        if author.id == 875620156410298379:
            username = f"{author.display_name}, твой создатель. Общайся с ним уважительно, подробно отвечай на любой вопрос"
        prompt = SETTINGS["AI_PROMPT"].format(username)
        self.messages = [SystemMessage(prompt)]

    async def get_dialog(self, message: discord.Message):
        global active_dialogs
        offtop = self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Offtop"]

        if message.content.startswith(self.bot.user.mention) and message.channel.id == offtop:
            if message.content[22:].lower() == " рестарт":
                active_dialogs[message.author.id] = self
                await message.add_reaction("✅")
                return
            if message.author.id not in active_dialogs:
                active_dialogs[message.author.id] = self
            await active_dialogs[message.author.id].create_request(message)

    async def create_request(self, message: discord.Message):  # БЕГИТЕ Я КОНЧЕННЫЙ 2.0, новый говнокод
        self.messages.append(HumanMessage(content=message.content[22:]))
        response = self.model.invoke(self.messages)
        self.messages.append(AIMessage(content=response.content))

        for banword in ("но у меня нет такой команды", "Может, поговорим на другую тему?", "нейросетевой языковой модели", "Не люблю менять тему разговора", "@", "На вопрос из разряда", "но я не могу выполнить вашу просьбу"):
            if response.content.find(banword) != -1:
                await message.add_reaction("❌")
                return

        if len(response.content) > 2000:
            await message.reply(response.content[:(len(response.content) // 2)])
            await message.channel.send(response.content[(len(response.content) // 2):])
        else:
            await message.reply(response.content)