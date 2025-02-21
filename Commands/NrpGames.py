import discord
import asyncio
from discord.ui import Select
from discord import app_commands as apc
from DataBase import DbWork
from typing import Literal
from random import choices, randint
from math import sqrt


class NrpGames(apc.Group, name="нрп_развлечение"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="снятие_заблокирован")
    async def clear_block(self, interaction: discord.Interaction, confirm: Literal["Да, я трачу 100 Нрп монет"]):
        """
        Покупка снятия роли "заблокирован" за 200 НонРП монет.
        """
        await interaction.response.defer()
        result_embed = discord.Embed(title="Снятие роли заблокирован.", colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        role = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['RpBlock'])

        if role not in interaction.user.roles:
            result_embed.description = "У вас нет роли \"Заблокирован\" для снятия."
            await interaction.followup.send(embed = result_embed)
            return
        if balance[0][0] < 200.0:
            result_embed.description = "У вас нет 200 НонРП монет."
            await interaction.followup.send(embed = result_embed)
            return

        DbWork.update("nrp", f"money = {balance[0][0] - 200}", f"userid = {interaction.user.id}")
        DbWork.delete("blocked", f"userid = {interaction.user.id}")

        await interaction.user.remove_roles(role)
        result_embed.description = "Успешно снята роль."
        await interaction.followup.send(embed = result_embed)


    @apc.command(name="поджечь_баланс")
    async def fire_balance(self, interaction: discord.Interaction, target: discord.Member, confirm: Literal["Да, я трачу 200 Нрп монет"]):
        """
        Попытка поджечь НонРП монеты другого пользователя.

        :param target: Пользователь, чей баланс вы пытаетесь поджечь.
        """
        await interaction.response.defer()
        result_embed = discord.Embed(title="Попытка Поджога!", colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        target_balance = DbWork.select("nrp", "money", f"WHERE userid = {target.id}")
        new_target_balance = target_balance[0][0]

        if balance[0][0] < 200.0:
            result_embed.description = "У вас нет 200 НонРП монет."
            await interaction.followup.send(embed = result_embed)
            return

        DbWork.update("nrp", f"money = {balance[0][0] - 200}", f"userid = {interaction.user.id}")

        if randint(1, 2) == 1:
            new_target_balance = new_target_balance * (randint(80, 95) / 100)
            result_embed.description = f"О ужас! Кошелёк {target.display_name} охватил огонь! Ему не удалось спасти {round(target_balance[0][0] - new_target_balance, 2)} монет..."
            DbWork.update("nrp", f"money = {new_target_balance}", f"userid = {target.id}")
            await interaction.followup.send(target.mention, embed = result_embed)
            return
        if randint(1, 2) == 1:
            new_balance = (balance[0][0] - 100) * (randint(80, 95) / 100)
            result_embed.description = f"Как же вам не повезло... Огонь охватил вас, и в пожаре сгорело {round(balance[0][0] - new_balance, 2)} монет..."
            DbWork.update("nrp", f"money = {new_balance}", f"userid = {interaction.user.id}")
            await interaction.followup.send(embed=result_embed)
            return
        result_embed.description = f"К сожалению, вам не повезло - огонь просто не успел разгореться, как тот потушили. Может быть, в следующий раз!"
        await interaction.followup.send(embed=result_embed)


    @apc.command(name="слоты")
    async def slot_game(self, interaction: discord.Interaction, game: Literal[3, 5], amount: float):
        """
        Крутка слотов.

        :param game: Режим игры.
        :param amount: Ваша ставка. От 25, до 50.
        """
        result_embed = discord.Embed(
            description=f" ### Крутятся слоты для {interaction.user.mention}! Ставка: {amount}\n",
            colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        balance = [[0.0]] if not balance else balance
        if amount <= 0.0:
            await interaction.response.send_message(f"Ставка не может быть меньше или равна нулю!", ephemeral=True)
            return
        if amount > 50.0 or amount < 25.0:
            await interaction.response.send_message(f"Ставка должна быть в диапазоне от 25 до 50 нрп монет!",
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
            series_reward = 4
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

        result_embed.description += f"Выигрыш: {gain}\n-# Баланс ИксКора: {round(bot_balance[0][0] - gain, 2)}"

        await message.edit(embed=result_embed)


async def setup(bot):
    bot.tree.add_command(NrpGames(bot), guild=bot.main_guild)
    print('Group loaded')