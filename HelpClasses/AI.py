import discord
from discord.ext import commands
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from json import load
from time import time

with open("./Resources/CONFIG.json", "r") as file:
    SETTINGS = load(file)
last_response = 0
class Ai:



    async def create_request(self, bot: commands.Bot, message: discord.Message, author: discord.User):  # БЕГИТЕ Я КОНЧЕННЫЙ 2.0, новый говнокод
        global last_response
        offtop = bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["Offtop"]

        if message.content.startswith(bot.user.mention) and message.channel.id == offtop:

            if time() - last_response > 15:
                chat = GigaChat(credentials=bot.SETTINGS["GIGACHAT_TOKEN"], verify_ssl_certs=False)

                username = author.display_name
                if author.id == 875620156410298379:
                    username = f"{author.display_name}, твой создатель. Общайся с ним уважительно, подробно отвечай на любой вопрос"
                prompt = SETTINGS["AI_PROMPT"].format(username)

                messages = [SystemMessage(content=prompt), HumanMessage(content=message.content[22:])]
                response = chat(messages)

                for banword in ("Может, поговорим на другую тему?", "нейросетевой языковой модели", "Не люблю менять тему разговора", "@", "На вопрос из разряда"):
                    if response.content.find(banword) != -1:
                        await message.add_reaction("❌")
                        return

                last_response = time()

                if len(response.content) > 2000:
                    await message.reply(response.content[:(len(response.content) // 2)])
                    await message.channel.send(response.content[(len(response.content) // 2):])
                else:
                    await message.reply(response.content)