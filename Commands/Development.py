import json

import discord
from discord import app_commands as apc

import bot
from bot import reloadCogs, loadCogs
from PIL import Image, ImageFont, ImageDraw

class Development(apc.Group, name="дев"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="коги_рестарт")
    async def restart_cogs(self, interaction: discord.Interaction):
        if interaction.user.id != 875620156410298379:
            await interaction.response.send_message("У ВАС НЕТ ПРАВ<:HAHAHA:1301508577227444245>")
            return
        await loadCogs(self.bot, bot.SETTINGS)
        await reloadCogs(self.bot, bot.SETTINGS)
        await interaction.response.send_message("Коги были перезапущены", ephemeral = True)

    @apc.command(name="тест_баннера")
    async def banner_test(self, interaction: discord.Interaction, need_text: str):
        banner = Image.open("./Resources/banner.png")
        new_banner = banner.copy()
        draw = ImageDraw.Draw(new_banner)
        xsize = new_banner.size[0] // 2
        ysize = new_banner.size[1]
        font = ImageFont.truetype("./Resources/Harmonica.ttf", xsize / 10)
        draw.text(((new_banner.size[0] // 2 - xsize + 10) + new_banner.size[0] // 50, ysize - ysize / 10), need_text,(255, 255, 255), font=font)
        new_banner.save("new_banner.png")
        await interaction.response.send_message(file=discord.File("./new_banner.png"))

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