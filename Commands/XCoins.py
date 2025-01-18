import discord
from discord import app_commands as apc
from DataBase import DbWork
from time import time
from typing import Literal

class SellButton(discord.ui.View):
    def __int__(self, user: discord.User, target: discord.User, price: float, xcoins: float):
        self.user = user
        self.target = target
        self.price = price
        self.xcoins = xcoins
        self.add_item(discord.ui.Button(label="Принять"))

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.success)
    async def AcceptButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("Вы не являетесь целью сделки!", ephemeral=True)
            return

        await interaction.response.edit_message(content="", view=None)
        target_nrp_balance = DbWork.select("nrp", "money", f"WHERE userid = {self.target.id}")[0][0]
        nrp_balance = DbWork.select("nrp", "money", f"WHERE userid = {self.user.id}")[0][0]

        if target_nrp_balance < self.price:
            await interaction.followup.send("У вас недостаточно Нрп монет для совершения сделки!", ephemeral=True)
            return

        target_balance = DbWork.select("xcoins", "coins", f"WHERE userid = {self.target.id}")
        if not target_balance:
            DbWork.insert("xcoins", ["userid", "coins", "miners"], [(self.target.id, self.xcoins, 0)])
        else:
            DbWork.update("xcoins", f"coins = {target_balance[0][0] + self.xcoins}", f"userid = {self.target.id}")

        balance = DbWork.select("xcoins", "coins", f"WHERE userid = {self.user.id}")
        DbWork.update("xcoins", f"coins = {balance[0][0] - self.xcoins}", f"userid = {self.user.id}")

        DbWork.update("nrp", f"money = {target_nrp_balance - self.price}", f"userid = {self.target.id}")
        DbWork.update("nrp", f"money = {nrp_balance + self.price}", f"userid = {self.user.id}")

        await interaction.message.reply("Транзакция совершена!")


class XCoins(apc.Group, name="икс_коины"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="история")
    async def xcoins(self, interaction: discord.Interaction):
        """
        Отображает историю недавних цен ПОСЛЕ СЖИГАНИЯ ИксКоина.
        """
        await interaction.response.defer()
        result_embed = discord.Embed(title="История стоимости ИксКоинов",
                                     colour=self.bot.SETTINGS["MAIN_COLOR"])
        sells = DbWork.select("xcoins_price", "price, time, reason", "WHERE reason = \"delete\" OR reason = \"random\" ORDER BY time LIMIT 40")
        actual_price = DbWork.select("xcoins_price", "price, time, reason", "ORDER BY time DESC LIMIT 1")
        result_embed.description = f"### Цена: {round(actual_price[0][0], 2)} XCoins"
        for price in sells:
            result_embed.description += f"\n- <t:{price[1]}:f> - {round(price[0], 2)}"
        await interaction.followup.send(embed=result_embed)

    @apc.command(name="баланс")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Отображает количество ИксКоинов Пользователя.

        :param user: Пользователь, чей баланс будет отображен.
        """
        await interaction.response.defer()

        price = DbWork.select("xcoins_price", "price, time, reason", "ORDER BY time DESC LIMIT 1")[0][0]
        user = interaction.user if user is None else user
        balance = DbWork.select("xcoins", "coins, miners", f"WHERE userid = {user.id}")
        balance = [[0.0, 0]] if not balance else balance

        result_embed = discord.Embed(
            description=f"### Баланс {user.mention}\n- **{round(balance[0][0], 2)}** XCoins -> {round(balance[0][0] * price, 2)} НонРП монет.\n- Майнеров: {balance[0][1]}",
            color=self.bot.SETTINGS["MAIN_COLOR"])
        await interaction.followup.send(embed=result_embed)

    @apc.command(name="рейтинг")
    async def rating(self, interaction: discord.Interaction):
        """
        Рейтинг из десяти самых богатых по ИксКоинам пользователей на сервере.
        """
        await interaction.response.defer()
        rating = DbWork.select("xcoins", "userid, coins", "ORDER BY coins DESC LIMIT 50")
        result_embed = discord.Embed(title="Криптоинвесторы всея Сервера:", description="", color=self.bot.SETTINGS["MAIN_COLOR"])

        i = 0
        for balance in rating:
            user = self.bot.get_user(balance[0])
            if user is None: continue
            if i == 10: break
            result_embed.description = result_embed.description + f"- {user.name} **: {balance[1]} XCoins**\n"
            i += 1
        await interaction.followup.send(embed=result_embed)

    @apc.command(name="продать")
    async def sell_xcoins(self, interaction: discord.Interaction, target: discord.Member, amount: float):
        """
        Предлагает покупку ИксКоинов другому пользователю.

        :param target: Пользователь, которому будет предложена покупка.
        :param amount: Количество ИксКоинов для продажи.
        """
        await interaction.response.defer()
        price = round(DbWork.select("xcoins_price", "price", "ORDER BY time DESC LIMIT 1")[0][0] * amount, 2)

        result_embed = discord.Embed(title=f"Продажа {amount} ИксКоинов.",
                                     description=f"Стоимость: {price} НонРП монет!",
                                     colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("xcoins", "coins", f"WHERE userid = {interaction.user.id}")[0][0]

        if balance < amount:
            result_embed.description = f"У вас нет {amount} ИксКоинов!"
            await interaction.followup.send(embed=result_embed)
            return
        if amount <= 0.0:
            result_embed.description = f"Нельзя передавать отрицательное количество ИксКоинов!"
            await interaction.followup.send(embed=result_embed)
            return
        if interaction.user.id == target.id:
            result_embed.description = f"Вы не можете продать ИксКоины себе!"
            await interaction.followup.send(embed=result_embed)
            return

        buttons = SellButton()  # Ебал я ваше ООП
        buttons.user = interaction.user  # Ебал я ваше ООП
        buttons.target = target  # Ебал я ваше ООП
        buttons.price = price  # Ебал я ваше ООП
        buttons.xcoins = amount  # Ебал я ваше ООП
        await interaction.followup.send(f"- Ожидание {target.mention}...", embed=result_embed, view=buttons)

    @apc.command(name="сжечь")
    async def delete_xcoins(self, interaction: discord.Interaction, amount: float):
        """
        Сжигает ИксКоины, чтобы их общее количество уменьшилось. Как следствие, повысится стоимость.

        :param amount: Число ИксКоинов для сжигания.
        """
        await interaction.response.send_message("Пока недоступно!", ephemeral=True)
        return
        await interaction.response.defer()
        result_embed = discord.Embed(title=f"Сжигание {amount} ИксКоинов.",
                                     colour=self.bot.SETTINGS["MAIN_COLOR"])

        balance = DbWork.select("xcoins", "coins", f"WHERE userid = {interaction.user.id}")[0][0]
        if balance < amount:
            result_embed.description = f"У вас нет {amount} ИксКоинов!"
            await interaction.followup.send(embed=result_embed)
            return
        if amount <= 1.0:
            result_embed.description = f"Нельзя сжечь значение менее единицы за раз!"
            await interaction.followup.send(embed=result_embed)
            return

        DbWork.update("xcoins", f"coins = {balance - amount}", f"userid = {interaction.user.id}")
        price = DbWork.select("xcoins_price", "price", "ORDER BY time LIMIT 1")

        coins = DbWork.select("xcoins", "coins")
        coins_amount = 0
        for coin in coins: coins_amount += coin[0]

        new_price = price[0][0] + amount / coins_amount * price[0][0]
        DbWork.insert("xcoins_price", ["price", "time", "reason"], [(new_price, int(time()), "delete")])
        result_embed.description = f"Новая цена за один ИксКоин: {round(new_price)}"
        await interaction.followup.send(embed = result_embed)


    @apc.command(name="купить_майнер")
    async def buy_miner(self, interaction: discord.Interaction, amount: int):
        """
        Покупает майнер, дающий ≈0.9 ИксКоина в день. Стоимость в нрп монетах = 2-ум ИксКоинам.

        :param amount: Количество майнеров для покупки. Стоимость в нрп монетах = 2-ум ИксКоинам.
        """
        await interaction.response.defer()
        result_embed = discord.Embed(title=f"Покупка {amount} майнера.",
                                     colour=self.bot.SETTINGS["MAIN_COLOR"])
        nrp_balance = DbWork.select("nrp", "money", f"WHERE userid = {interaction.user.id}")
        balance = DbWork.select("xcoins", "coins, miners", f"WHERE userid = {interaction.user.id}")
        if not balance:
            DbWork.insert("xcoins", ["userid", "coins", "miners"], [(interaction.user.id, 0.0, 0)])
            balance = ((0.0, 0),)
        price = DbWork.select("xcoins_price", "price", "ORDER BY time DESC LIMIT 1")[0][0] * 2 * amount

        if nrp_balance[0][0] < price:
            result_embed.description = f"У вас нет {price} НонРП монет для оплаты!"
            await interaction.followup.send(embed=result_embed)
            return
        if amount <= 0:
            result_embed.description = f"Нельзя купить отрицательное количество майнеров!"
            await interaction.followup.send(embed=result_embed)
            return

        DbWork.update("nrp", f"money = {nrp_balance[0][0] - price}", f"userid = {interaction.user.id}")
        DbWork.update("xcoins", f"miners = {balance[0][1] + amount}", f"userid = {interaction.user.id}")

        result_embed.description = f"Добавлено {amount} майнеров в ваш инвентарь!"
        await interaction.followup.send(embed = result_embed)


async def setup(bot):
    bot.tree.add_command(XCoins(bot), guild=bot.main_guild)
    print('Group loaded')
