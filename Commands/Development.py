import json

import discord
from discord import app_commands as apc
from datetime import datetime
from bot import reloadCogs, loadCogs
from PIL import Image, ImageFont, ImageDraw
from DataBase import DbWork
from random import choices
from math import sqrt
from typing import Literal
import asyncio

class Development(apc.Group, name="дев"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="коги_рестарт")
    @apc.checks.has_permissions(administrator=True)
    async def restart_cogs(self, interaction: discord.Interaction):
        if interaction.user.id != 875620156410298379:
            await interaction.response.send_message("У ВАС НЕТ ПРАВ<:HAHAHA:1301508577227444245>")
            return
        await interaction.response.send_message("Коги будут перезапущены", ephemeral = True)
        await loadCogs(self.bot, self.bot.SETTINGS)
        await reloadCogs(self.bot, self.bot.SETTINGS)


    @apc.command(name="тест")
    @apc.checks.has_permissions(administrator=True)
    async def test(self, interaction: discord.Interaction):
        DbWork.delete("characters", f"userid = {interaction.user.id}")
        x = DbWork.select("characters", "name", f"WHERE userid = {interaction.user.id}")
        print(x)

    @apc.command(name="получить_промпт")
    async def get_prompt(self, interaction: discord.Interaction):
        if not interaction.user.id in [1096817786229108796, 875620156410298379]:
            await interaction.response.send_message("У ВАС НЕТ ПРАВ<:HAHAHA:1301508577227444245>")
            return
        with open("./Resources/CONFIG.json", "r") as file:
            config = json.load(file)
        await interaction.response.send_message(config["AI_PROMPT"], ephemeral=True)

    @apc.command(name="изменить_промпт")
    async def change_prompt(self, interaction: discord.Interaction, text: str):
        if not interaction.user.id in [1096817786229108796, 875620156410298379]:
            await interaction.response.send_message("У ВАС НЕТ ПРАВ<:HAHAHA:1301508577227444245>")
            return
        with open("./Resources/CONFIG.json", "r") as file:
            config = json.load(file)
        config["AI_PROMPT"] = text
        with open("../Resources/CONFIG.json", "w") as file:
            json.dump(config, file, indent=3)
        await interaction.response.send_message("Промпт успешно изменён. Новая версия:\n" + text, ephemeral = True)

async def setup(bot):
    bot.tree.add_command(Development(bot), guild=bot.dev_guild)
    print('Group loaded')