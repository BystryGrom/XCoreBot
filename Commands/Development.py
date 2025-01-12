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

    @apc.command(name="слоты")
    @apc.checks.has_permissions(administrator=True)
    async def slot_game(self, interaction: discord.Interaction, game: Literal[3, 5], amount: float):
        result_embed = discord.Embed(description=f" ### Крутятся слоты для {interaction.user.mention}! Ставка: {amount}\n", colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        balance = [[0.0]] if not balance else balance
        if amount <= 0.0:
            await interaction.response.send_message(f"Ставка не может быть меньше или равна нулю!", ephemeral=True)
            return
        if balance[0][0] < amount:
            await interaction.response.send_message(f"У вас нет {amount} монет!", ephemeral=True)
            return

        await interaction.response.send_message("Запуск рулеточки!", ephemeral = True)
        message = await interaction.channel.send(embed = result_embed)

        elements = ("🔴", "🟠", "🟡", "🟢", "🔵", "🖤", "🤍")
        chances = (400, 400, 400, 400, 400, 1, 1)
        seq = choices(elements, chances, k=game**2)
        await asyncio.sleep(0.5)

        i = 1
        last_element = ""
        series = [0]
        for element in seq:
            if last_element == element:
                series.append((series[-1] + 1) ** 2)
            else: series.append(0)
            result_embed.description += element
            if i % game == 0:
                result_embed.description += "\n# "
                await message.edit(embed = result_embed)
                await asyncio.sleep(0.5)
            last_element = element
            i += 1

        print(series)
        gain = sum(series) * amount / (amount ** 2) - amount
        result_embed.description += f"\n\n# Выигрышь: {gain}"
        await message.edit(embed=result_embed)

async def setup(bot):
    bot.tree.add_command(Development(bot), guild=bot.dev_guild)
    print('Group loaded')