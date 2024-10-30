import discord
from discord import app_commands as apc
from Resources import Config
from bot import reloadCogs, loadCogs
from PIL import Image, ImageFont, ImageDraw

class Development(apc.Group, name="дев"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="коги_рестарт")
    async def restart_cogs(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await loadCogs(self.bot)
        await reloadCogs(self.bot)
        await interaction.followup.send("Коги были перезапущены", ephemeral = True)

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



async def setup(bot):
    bot.tree.add_command(Development(bot), guild=Config.devServer)
    print('Group loaded')