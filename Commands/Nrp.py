import discord
import asyncio
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
        balance = DbWork.select("nrp", "money", f"WHERE userid = {user.id}")
        balance = [[0.0]] if not balance else balance

        result_embed = discord.Embed(description=f"### Баланс {user.mention}\n- **{round(balance[0][0], 2)}**<a:coins:1300835076602593280>", color=self.bot.SETTINGS["MAIN_COLOR"])
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
        rating = DbWork.select("nrp", "userid, money", "ORDER BY money DESC LIMIT 50")
        result_embed = discord.Embed(title="Богачи Сервера:", description = "", color=self.bot.SETTINGS["MAIN_COLOR"])

        i = 0
        for balance in rating:
            user = self.bot.get_user(balance[0])
            if user is None: continue
            if i == 10: break
            result_embed.description = result_embed.description + f"- {user.name} **: {balance[1]}**\n"
            i += 1
        await interaction.followup.send(embed = result_embed)

    @apc.command(name="переключить_серию")
    async def permission_to_change_nickname(self, interaction: discord.Interaction, mode: Literal["Yes(Virgin)", "No(Slave)"]):
        """
        Переключает автоматическое изменение ника для отображения серии активности.
        
        :param mode: Режим для включения (выбор очевиден, Yes)
        """
        
        await interaction.response.defer()
        result_embed = discord.Embed(title="Режим отображения НонРП серии", description="У вас итак стоит этот режим!", color=self.bot.SETTINGS["MAIN_COLOR"])
        role = interaction.guild.get_role(1328382608970743899)
        if mode == "Yes(Virgin)":
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                result_embed.description = "### Отображение включено! Sigma!"
        else:
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                result_embed.description = "### Отображение выключено. Увы."
        await interaction.followup.send(embed=result_embed)

    @apc.command(name="слоты")
    async def slot_game(self, interaction: discord.Interaction, game: Literal[3, 5], amount: float):
        result_embed = discord.Embed(
            description=f" ### Крутятся слоты для {interaction.user.mention}! Ставка: {amount}\n",
            colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        balance = [[0.0]] if not balance else balance
        if amount <= 0.0:
            await interaction.response.send_message(f"Ставка не может быть меньше или равна нулю!", ephemeral=True)
            return
        if amount > 50.0 or amount < 10.0:
            await interaction.response.send_message(f"Ставка должна быть в диапазоне от 10 до 50 нрп монет!",
                                                    ephemeral=True)
            return
        if balance[0][0] < amount:
            await interaction.response.send_message(f"У вас нет {amount} монет!", ephemeral=True)
            return

        await interaction.response.send_message("Запуск рулеточки!", ephemeral=True)
        message = await interaction.channel.send(embed=result_embed)

        elements = ("🔴", "🟠", "🟡", "🟢", "🔵", "🖤", "🤍")
        chances = (300, 300, 300, 300, 300, 1, 1)
        seq = choices(elements, chances, k=game ** 2)
        await asyncio.sleep(0.5)

        if game == 3:
            series_reward = 5
        else:
            series_reward = 1.5

        i = 1
        last_element = ""
        series = [0]
        result_embed.description += "\n# "
        for element in seq:
            if last_element == element:
                series.append((series[-1] + series_reward) * 1.35)
            elif element == "🖤":
                series.append(-50)
            elif element == "🤍":
                series.append(25)
            else:
                series.append(0)

            result_embed.description += element
            last_element = element
            if i % game == 0:
                await message.edit(embed=result_embed)
                await asyncio.sleep(0.5)
                result_embed.description += "\n# "
                last_element = ""
            i += 1

        gain = sum(series) * sqrt(amount) - sqrt(amount) * (game + sqrt(amount))
        if game == 3:
            gain + abs(gain) / 2
        else:
            gain - abs(gain) / 2
        gain = round(gain, 2)

        balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        DbWork.update("nrp", f"money = {balance[0][0] + gain}", f"userid = {interaction.user.id}")
        bot_balance = DbWork.select("nrp", "money", f"WHERE userid = {self.bot.user.id}")
        DbWork.update("nrp", f"money = {bot_balance[0][0] - gain}", f"userid = {self.bot.user.id}")

        result_embed.description += f"Выигрышь: {gain}\n-# Баланс ИксКора: {round(bot_balance[0][0] - gain, 2)}"

        await message.edit(embed=result_embed)


async def setup(bot):
    bot.tree.add_command(Nrp(bot), guild=bot.main_guild)
    print('Group loaded')