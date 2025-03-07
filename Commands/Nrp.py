import discord
import asyncio
from discord.ui import Select
from discord import app_commands as apc
from DataBase import DbWork
from typing import Literal
from random import choices
from math import sqrt

class Nrp(apc.Group, name="нрп"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="баланс")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Отображает НонРП баланс Пользователя.

        :param user: Пользователь, чей баланс будет отображен.
        """
        await interaction.response.defer()

        user = interaction.user if user is None else user
        balance = DbWork.select("nrp", "money, series", f"WHERE userid = {user.id}")
        balance = [[0.0]] if not balance else balance

        result_embed = discord.Embed(description=f"### Баланс {user.mention}\n- **{round(balance[0][0], 2)}**<a:coins:1300835076602593280>\n- Серия из {balance[0][1]} активных дней🔥", colour=self.bot.SETTINGS["MAIN_COLOR"])
        if user.id in self.bot.SETTINGS["Premium"]:
            result_embed.colour = self.bot.SETTINGS["PREMIUM_COLOR"]
            result_embed.description += f"\n\n- {user.name} владеет премиумом!🔓"
        await interaction.followup.send(embed = result_embed)

    @apc.command(name="установить_баланс")
    @apc.checks.has_permissions(administrator=True)
    async def set_balance(self, interaction: discord.Interaction, user: discord.Member, balance: float):
        DbWork.update("nrp", f"money = {balance}", f"userid = {user.id}")
        await interaction.response.send_message(f"Баланс {user.mention} установлен на: {balance}")

    @apc.command(name="рейтинг")
    async def rating(self, interaction: discord.Interaction):
        """
        Рейтинг из десяти самых богатых по НонРП валюте пользователей на сервере
        """
        await interaction.response.defer()
        rating = DbWork.select("nrp", "userid, money", "ORDER BY money DESC")
        balance = DbWork.select("nrp", "userid, money", f"WHERE userid = {interaction.user.id}")
        result_embed = discord.Embed(title="Богачи Сервера:", description = f"## Ваше положение: {rating.index(balance[0])}\n")
        result_embed.colour = self.bot.SETTINGS["PREMIUM_COLOR"] if interaction.user.id in self.bot.SETTINGS["Premium"] else self.bot.SETTINGS["MAIN_COLOR"]

        i = 0
        for count in range(50):
            user = self.bot.get_user(rating[count][0])
            if user is None: continue
            if i == 10: break
            result_embed.description = result_embed.description + f"- {user.name} **: {rating[count][1]}**<a:coins:1300835076602593280>\n"
            i += 1
        await interaction.followup.send(embed = result_embed)


async def setup(bot):
    bot.tree.add_command(Nrp(bot), guild=bot.main_guild)
    print('Group loaded')