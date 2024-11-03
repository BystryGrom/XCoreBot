from discord.ext import commands
from discord import Activity
import discord.ui
import discord
import os
import json
from discord.ext.commands import ExtensionAlreadyLoaded

with open("Resources/CONFIG.json", "r") as file:
    SETTINGS = json.load(file)


async def loadCogs(Bot, settings):
    # Загрузка Commands
    for filename in os.listdir('Commands'):
        if filename.endswith('.py'):
            try:
                await Bot.load_extension(f'Commands.{filename[:-3]}')
            except ExtensionAlreadyLoaded:
                pass

    await Bot.tree.sync(guild=discord.Object(id=settings['Guilds']['MAIN_GUILD']["guild_id"]))
    print("Команды синхронизированы")

    # Загрузка Cogs
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            try:
                await Bot.load_extension(f'Cogs.{filename[:-3]}')
            except ExtensionAlreadyLoaded:
                pass


async def reloadCogs(Bot, settings):
    # Перезагрузка Commands
    for filename in os.listdir('Commands'):
        if filename.endswith('.py'):
            await Bot.reload_extension(f'Commands.{filename[:-3]}')

    await Bot.tree.sync(guild=discord.Object(id=settings['Guilds']['MAIN_GUILD']["guild_id"]))
    print("Команды синхронизированы")

    # Перезагрузка Cogs
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            await Bot.reload_extension(f'Cogs.{filename[:-3]}')


# Класс бота
class MyBot(commands.Bot):
    async def on_ready(self):
        await bot_object.change_presence(status=discord.Status.online, activity=Activity(name='КОФЕ!', type=discord.ActivityType.playing))
        print(f'{bot_object.user} жив!')

        self.SETTINGS = SETTINGS
        self.main_guild = discord.Object(id=SETTINGS['Guilds']['MAIN_GUILD']["guild_id"])
        self.dev_guild = discord.Object(id=SETTINGS['Guilds']['DEV_GUILD']["guild_id"])

        await loadCogs(bot_object, SETTINGS)


bot_object = MyBot(command_prefix='.', help_command=None, intents=discord.Intents.all())  # Инициализация бота

def bot_start():
    bot_object.run(SETTINGS["TOKEN"])


if __name__ == '__main__':
    bot_start()
