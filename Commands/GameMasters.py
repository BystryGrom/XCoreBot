import discord
from discord import app_commands as apc
from DataBase import DbWork
from datetime import datetime, timedelta
from typing import Literal
from time import time
from asyncio import sleep

class GameMasters(apc.Group, name="мастер"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="закрыть_тикет")
    @apc.checks.has_permissions(manage_channels=True)
    async def close_ticket(self, interaction: discord.Interaction):
        """
        Закрывает тикет, удаляя его канал.
        """
        await interaction.response.defer()

        if interaction.channel.category.id != self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Categories"]["MasterTickets"]:
            await interaction.followup.send("Вы находитесь вне тикета!")
            return
        await interaction.followup.send("Тикет будет удалён через 10 секунд!")
        await sleep(10)
        await interaction.channel.delete(reason="Закрытие тикета")

    @apc.command(name="выдать_предмет")
    @apc.checks.has_permissions(manage_roles=True)
    async def add_item(self, interaction: discord.Interaction, user: discord.Member, name: str, desc: str, amount: int):
        """
        Выдает предмет/ы Пользователю в РП инвентарь.

        :param user: Пользователь, которому будет выдан предмет/ы.
        :param name: Название предмета.
        :param desc: Описание предмета.
        :param amount: Количество предметов.
        """
        await interaction.response.defer()

        item = DbWork.select("inventories", "amount", f"WHERE userid = {user.id} AND name = '{name}'")
        result_embed = discord.Embed(
            description=f"### Выдача \"{name}\" {user.mention}\n- **Описание:** {desc}\n- **Количество:** {amount}",
            colour=self.bot.SETTINGS["PREMIUM_COLOR"] if interaction.user.id in self.bot.SETTINGS["Premium"] else
            self.bot.SETTINGS["MAIN_COLOR"])

        if not item:
            DbWork.insert("inventories", ["userid", "name", "description", "amount"], [(user.id, name, desc, amount)])
        else:
            DbWork.update("inventories", f"amount = {item[0][0] + amount}", f"userid = {user.id} AND name = '{name}'")

        await self.logs.addItem(interaction.user, user, name, desc, amount)

        await interaction.followup.send(embed=result_embed)

    @apc.command(name="добавить_валюту")
    @apc.checks.has_permissions(manage_roles=True)
    async def add_currency(self, interaction: discord.Interaction, user: discord.Member, amount: int, currency: str):
        """
        Добавляет РП валюту пользователю. Доступна Мастерам.

        :param user: Пользователь, баланс которого вы желаете изменить.
        :param amount: Число валюты для добавления. (Используйте отрицательное для снятия)
        :param currency: Валюта.
        """
        await interaction.response.defer()

        old_money = DbWork.select("economy", "money", f"WHERE userid = {user.id} AND currency = '{currency}'")

        if not old_money:
            DbWork.insert("economy", ["userid", "money", "currency"], [(user.id, amount, currency)])
        elif old_money[0][0] + amount == 0:
            DbWork.delete("economy", f"userid = {user.id} AND currency = '{currency}'")
        else:
            DbWork.update("economy", f"money = {old_money[0][0] + amount}",
                          f"userid = {user.id} AND currency = '{currency}'")

        await self.logs.addCurrency(interaction.user, user, amount, currency)

        result_embed = discord.Embed(
            description=f"### Изменение РП валюты {user.mention}\n- **{amount} {currency} успешно добавлено.**")
        result_embed.colour = self.bot.SETTINGS["PREMIUM_COLOR"] if interaction.user.id in self.bot.SETTINGS[
            "Premium"] else self.bot.SETTINGS["MAIN_COLOR"]
        await interaction.followup.send(embed=result_embed)

    @apc.command(name="очистить_заблокированных")
    @apc.checks.has_permissions(manage_roles=True)
    async def clear_blocked(self, interaction: discord.Interaction):
        """
        Снимает роль "заблокирован" у зарегистрированных через бота пользователей
        """
        await interaction.response.send_message("Начало очистки...")
        blocked = DbWork.select("blocked")
        rp_block = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['RpBlock'])

        count = 0
        for userid in blocked:
            user = interaction.guild.get_member(userid[0])
            if user is not None:
                await user.remove_roles(rp_block)
            DbWork.delete("blocked", f"userid = {userid[0]}")
            count += 1

        await interaction.channel.send(f"Очистка завершена. Снято \"Заблокирован\": {count}")

async def setup(bot):
    bot.tree.add_command(GameMasters(bot), guild=bot.main_guild)
    print('Group loaded')
