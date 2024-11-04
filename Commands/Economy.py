import discord
from discord import app_commands as apc
from DataBase import DbWork


class Economy(apc.Group, name="экономика"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="кошелёк")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        user = interaction.user if user is None else user
        balance = DbWork.select("economy", "money, currency", f"WHERE userid = {user.id}")

        result_embed = discord.Embed(description=f"### РП валюта {user.mention}", color=self.bot.SETTINGS["MAIN_COLOR"])
        if not balance: result_embed.description = result_embed.description + "\n- Отсутствует"

        for currency in balance:
            result_embed.description = result_embed.description + f"\n- {currency[0]} **{currency[1]}**"

        await interaction.response.send_message(embed=result_embed)


    @apc.command(name="добавить_валюту")
    async def add_currency(self, interaction: discord.Interaction, user: discord.Member, amount: int, currency: str):
        old_money = DbWork.select("economy", "money", f"WHERE userid = {user.id} AND currency = '{currency}'")

        if not old_money:
            DbWork.insert("economy", ["userid", "money", "currency"], [(user.id, amount, currency)])
        elif old_money[0][0] + amount == 0:
            DbWork.delete("economy", f"userid = {user.id} AND currency = '{currency}'")
        else:
            DbWork.update("economy", f"money = {old_money[0][0] + amount}", f"userid = {user.id} AND currency = '{currency}'")

        result_embed = discord.Embed(description=f"### Изменение РП валюты {user.mention}\n- **{amount} {currency} успешно добавлено.**", color=self.bot.SETTINGS["MAIN_COLOR"])
        await interaction.response.send_message(embed = result_embed)


    @apc.command(name="передать_валюту")
    async def give_currency(self, interaction: discord.Interaction, target: discord.Member, amount: int, currency: str):
        user = interaction.user
        old_money = DbWork.select("economy", "money", f"WHERE userid = {user.id} AND currency = '{currency}'")
        target_old_money = DbWork.select("economy", "money", f"WHERE userid = {target.id} AND currency = '{currency}'")

        result_embed = discord.Embed(description=f"### Передача валюты {user.mention} к {target.mention}\n- {amount} **{currency}** успешно переданы {target.display_name}",
                                     color=self.bot.SETTINGS["MAIN_COLOR"])

        if not old_money:
            await interaction.response.send_message(f"У вас нет {currency}!", ephemeral = True)
            return
        elif old_money[0][0] < amount:
            await interaction.response.send_message(f"У вас недостаточно {currency}!", ephemeral=True)
            return
        elif amount <= 0:
            await interaction.response.send_message(f"Нельзя передавать отрицательное количество валюты!", ephemeral=True)
            return
        await interaction.response.send_message(embed = result_embed)

        DbWork.update("economy", f"money = {old_money[0][0] - amount}", f"userid = {user.id} AND currency = '{currency}'")

        if not target_old_money:
            DbWork.insert("economy", ["userid", "money", "currency"], [(target.id, amount, currency)])
        else:
            DbWork.update("economy", f"money = {target_old_money[0][0] + amount}", f"userid = {target.id} AND currency = '{currency}'")

    @apc.command(name="инвентарь")
    async def inventory(self, interaction: discord.Interaction, user: discord.Member = None, page: int = 1):
        user = interaction.user if user is None else user
        inventory = DbWork.select("inventories", "name, description, amount", f"WHERE userid = {user.id}")
        result_embed = discord.Embed(description=f"## Инвентарь {user.mention}", colour=self.bot.SETTINGS["MAIN_COLOR"])
        if not inventory:
            result_embed.description += "\n- **Предметы отсутствуют!**"
            await interaction.response.send_message(embed=result_embed)
            return

        i = 0
        for item in inventory:
            if i < page * 10 and i >= (i - 1) * 10:
                result_embed.add_field(name=item[0], value=f"Описание: {item[1]}\nКоличество: {item[2]}", inline=False)
            i += 1

        await interaction.response.send_message(embed=result_embed)

    @apc.command(name="выдать_предмет")
    async def add_item(self, interaction: discord.Interaction, user: discord.Member, name: str, desc: str, amount: int):
        item = DbWork.select("inventories", "amount", f"WHERE userid = {user.id} AND name = '{name}'")
        result_embed = discord.Embed(
            description=f"### Выдача \"{name}\" {user.mention}\n- **Описание:** {desc}\n- **Количество:** {amount}",
            colour=self.bot.SETTINGS["MAIN_COLOR"])
        if not item:
            DbWork.insert("inventories", ["userid", "name", "description", "amount"], [(user.id, name, desc, amount)])
        else:
            DbWork.update("inventories", f"amount = {item[0][0] + amount}", f"userid = {user.id} AND name = '{name}'")

        await interaction.response.send_message(embed=result_embed)

    @apc.command(name="передать_предмет")
    async def give_item(self, interaction: discord.Interaction, target: discord.Member, name: str, amount: int):
        sender_item = DbWork.select("inventories", "name, description, amount",
                                    f"WHERE userid = {interaction.user.id} AND name = '{name}'")
        if not sender_item:
            await interaction.response.send_message(f"У вас нет предмета с названием \"{name}\"!", ephemeral=True)
            return
        elif amount < 1:
            await interaction.response.send_message(f"Нельзя передавать отрицательное количество предмета!",
                                                    ephemeral=True)
            return
        elif sender_item[0][2] < amount:
            await interaction.response.send_message(f"У вас недостаточно \"{name}\"!", ephemeral=True)
            return

        await interaction.response.defer()

        if sender_item[0][2] == amount:
            DbWork.delete("inventories", f"userid = {interaction.user.id} AND name = '{name}'")
        else:
            print("upd")
            DbWork.update("inventories", f"amount = {sender_item[0][2] - amount}",
                          f"userid = {interaction.user.id} AND name = '{name}'")

        target_item = DbWork.select("inventories", "name, description, amount",
                                    f"WHERE userid = {target.id} AND name = '{name}'")
        result_embed = discord.Embed(
            description=f"### Передача \"{name}\"\n### {interaction.user.mention} -> {target.mention}\n- **Описание:** {sender_item[0][1]}\n- **Количество:** {amount}",
            colour=self.bot.SETTINGS["MAIN_COLOR"])
        if not target_item:
            DbWork.insert("inventories", ["userid", "name", "description", "amount"],
                          [(target.id, name, sender_item[0][1], amount)])
        else:
            DbWork.update("inventories", f"amount = {target_item[0][2] + amount}",
                          f"userid = {target.id} AND name = '{name}'")

        await interaction.followup.send(embed=result_embed)

async def setup(bot):
    bot.tree.add_command(Economy(bot), guild=bot.main_guild)
    print('Group loaded')
