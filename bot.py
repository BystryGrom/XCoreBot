from discord.ext import commands
from discord import Activity
import discord.ui
import discord
import os

from discord.ext.commands import ExtensionAlreadyLoaded

from Resources.Config import TOKEN, mainServer

async def loadCogs(Bot):
    # Загрузка Commands
    for filename in os.listdir('Commands'):
        if filename.endswith('.py'):
            try: await Bot.load_extension(f'Commands.{filename[:-3]}')
            except ExtensionAlreadyLoaded: pass

    await Bot.tree.sync(guild=mainServer)
    print("Команды синхронизированы")

    # Загрузка Cogs
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            try: await Bot.load_extension(f'Cogs.{filename[:-3]}')
            except ExtensionAlreadyLoaded: pass

async def reloadCogs(Bot):
    # Перезагрузка Commands
    for filename in os.listdir('Commands'):
        if filename.endswith('.py'):
            await Bot.reload_extension(f'Commands.{filename[:-3]}')

    await Bot.tree.sync(guild=mainServer)
    print("Команды синхронизированы")

    # Перезагрузка Cogs
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            await Bot.reload_extension(f'Cogs.{filename[:-3]}')


# Класс бота
class MyBot(commands.Bot):
    async def on_ready(self):
        await bot_object.change_presence(status=discord.Status.online,
                                         activity=Activity(name='КОФЕ!', type=discord.ActivityType.playing))
        print(f'{bot_object.user} жив!')

        await loadCogs(bot_object)

bot_object = MyBot(command_prefix='.', help_command=None, intents=discord.Intents.all()) # Инициализация бота

def bot_start():
    bot_object.run(TOKEN)

if __name__ == '__main__':
    bot_start()
