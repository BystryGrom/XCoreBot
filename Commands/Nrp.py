import discord
from discord import app_commands as apc
from DataBase import DbWork

class Nrp(apc.Group, name="нрп"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="баланс")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        user = interaction.user if user is None else user
        balance = DbWork.select("nrp", "money", f"WHERE userid = {user.id}")
        balance = [[0.0]] if not balance else balance
        result_embed = discord.Embed(description=f"### Баланс {user.mention}\n- **{round(balance[0][0], 2)}**<a:coins:1300835076602593280>", color=self.bot.SETTINGS["MAIN_COLOR"])
        await interaction.response.send_message(embed = result_embed)

    @apc.command(name="рейтинг")
    async def rating(self, interaction: discord.Interaction):
        rating = DbWork.select("nrp", "userid, money", "ORDER BY money DESC LIMIT 10")
        result_embed = discord.Embed(title="Богачи Сервера:", description="", color=self.bot.SETTINGS["MAIN_COLOR"])
        for balance in rating:
            result_embed.description = result_embed.description + f"- {self.bot.get_user(balance[0]).name} **: {balance[1]}**\n"
        await interaction.response.send_message(embed = result_embed)

    @apc.command(name="инвентарь")
    async def inventory(self, interaction: discord.Interaction, user: discord.Member = None, page: int = 1):
        user = interaction.user if user is None else user
        inventory = DbWork.select("inventories", "name, description, amount", f"WHERE userid = {user.id}")
        result_embed = discord.Embed(description=f"## Инвентарь {user.mention}", colour=self.bot.SETTINGS["MAIN_COLOR"])
        if not inventory:
            result_embed.description += "\n- **Предметы отсутствуют!**"
            await interaction.response.send_message(embed = result_embed)
            return

        i = 0
        for item in inventory:
            if i < page * 10 and i >= (i - 1) * 10:
                result_embed.add_field(name=item[0], value=f"Описание: {item[1]}\nКоличество: {item[2]}", inline=False)
            i += 1

        await interaction.response.send_message(embed = result_embed)

    @apc.command(name="выдать_предмет")
    async def add_item(self, interaction: discord.Interaction, user: discord.Member, name: str, desc: str, amount: int):
        item = DbWork.select("inventories", "amount", f"WHERE userid = {user.id} AND name = '{name}'")
        result_embed = discord.Embed(description=f"### Выдача {name} {user.mention}\n- **Описание:** {desc}\n- **Количество:** {amount}",
                                     colour=self.bot.SETTINGS["MAIN_COLOR"])
        if not item:
            DbWork.insert("inventories", ["userid", "name", "description", "amount"], [(user.id, name, desc, amount)])
        else:
            DbWork.update("inventories", f"amount = {item[0][0] + amount}", f"userid = {user.id} AND name = '{name}'")

        await interaction.response.send_message(embed = result_embed)


async def setup(bot):
    bot.tree.add_command(Nrp(bot), guild=bot.main_guild)
    print('Group loaded')