import discord
from discord import app_commands as apc
from DataBase import DbWork
from Resources import Config


class Economy(apc.Group, name="экономика"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="кошелёк")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        user = interaction.user if user is None else user
        balance = DbWork.select("economy", "money, currency", f"WHERE userid = {user.id}")

        result_embed = discord.Embed(description=f"### РП валюта {user.mention}", colour=Config.mainColor)
        if not balance: result_embed.description = result_embed.description + "\n- Отсутствует"

        for currency in balance:
            result_embed.description = result_embed.description + f"\n- {currency[0]} **{currency[1]}**"

        await interaction.response.send_message(embed=result_embed)


    @apc.command(name="добавить_валюту")
    async def add_currency(self, interaction: discord.Interaction, user: discord.Member, amount: int, currency: str):
        old_money = DbWork.select("economy", "money", f"WHERE userid = {user.id} AND currency = '{currency}'")

        if not old_money:
            DbWork.insert("economy", ["userid", "money", "currency"], [(user.id, amount, currency)])
        else:
            DbWork.update("economy", f"money = {old_money[0][0] + amount}", f"userid = {user.id} AND currency = '{currency}'")

        result_embed = discord.Embed(description=f"### Изменение РП валюты {user.mention}\n- **{amount} {currency} успешно добавлено.**", colour=Config.mainColor)
        await interaction.response.send_message(embed = result_embed)


    @apc.command(name="передать_валюту")
    async def give_currency(self, interaction: discord.Interaction, target: discord.Member, amount: int, currency: str):
        await interaction.response.defer()
        user = interaction.user
        old_money = DbWork.select("economy", "money", f"WHERE userid = {user.id} AND currency = '{currency}'")

        if not old_money:
            await interaction.followup.send(f"У вас нет {currency}!", ephemeral = True)
            return
        elif old_money[0][0] < amount:
            await interaction.followup.send(f"У вас недостаточно {currency}!", ephemeral=True)
            return

        DbWork.update("economy", f"money = {old_money[0][0] - amount}", f"userid = {user.id} AND currency = '{currency}'")

        target_old_money = DbWork.select("economy", "money", f"WHERE userid = {target.id} AND currency = '{currency}'")

        if not target_old_money:
            DbWork.insert("economy", ["userid", "money", "currency"], [(target.id, amount, currency)])
        else:
            DbWork.update("economy", f"money = {target_old_money[0][0] + amount}", f"userid = {target.id} AND currency = '{currency}'")

        result_embed = discord.Embed(description=f"### Передача валюты {user.mention} к {target.mention}\n- {amount} **{currency}** успешно переданы {target.display_name}",
                                     colour=Config.mainColor)

        await interaction.followup.send(embed = result_embed)


async def setup(bot):
    bot.tree.add_command(Economy(bot), guild=Config.mainServer)
    print('Group loaded')
