import discord
from discord import app_commands as apc
from Resources import Config
from DataBase import DbWork


class Moderation(apc.Group, name="мод"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="варн")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, grade: int, reason: str):
        if grade < 1:
            await interaction.response.send_message("Кол-во баллов не может быть отрицательным.", ephemeral = True)
            return

        warns = DbWork.select("warns", "id, grade", f"WHERE userid = {user.id} ORDER BY id")
        id = 1 if not warns else warns[-1][0] + 1

        DbWork.insert("warns",
                      ["id", "userid", "grade", "reason"],
                      [(id, user.id, grade, reason)])

        result_grade = grade
        for warn in warns: result_grade += warn[1]

        result_embed = discord.Embed(title="Выдача Варна", description=f"> Варн № {id} пользователя {user.mention}\n- Вес: {grade}\n- Причина: {reason}", color=Config.mainColor)

        if result_grade >= 10:
            result_embed.description = result_embed.description + "\n\n### - Превышен лимит баллов. Выдан бан."

        await interaction.response.send_message(embed = result_embed)

    @apc.command(name="удалить_варн")
    async def remove_warn(self, interaction: discord.Interaction, user: discord.Member, id: int):
        warn = DbWork.select("warns", "grade, reason", f"WHERE id = {id} AND userid = {user.id}")
        if not warn:
            await interaction.response.send_message("Warn was not found.", ephemeral = True)
            return
        DbWork.delete("warns", f"id = {id} AND userid = {user.id}")
        result_embed = discord.Embed(title="Удаление варна", description=f"> Удалён варн № {id} пользователя {user.mention}\n- Вес: {warn[0][0]}\n- Причина: {warn[0][1]}", color=Config.mainColor)
        await interaction.response.send_message(embed = result_embed)


    @apc.command(name="варны")
    async def warns(self, interaction: discord.Interaction, user: discord.Member):
        warns = DbWork.select("warns", "id, grade, reason", f"WHERE userid = {user.id}")
        if not warns:
            await interaction.response.send_message("No warns")
            return

        result_grade = 0
        text_warns = ""
        for warn in warns:
            result_grade += warn[1]
            text_warns += f"\n№ {warn[0]} - {' ●' * warn[1]}: {warn[2]}"
        result_embed = discord.Embed(title="",
                                     description=f"# {' **●**' * result_grade}{' **○**' * (10 - result_grade)}\n" + text_warns,
                                     colour=Config.mainColor)

        await interaction.response.send_message(embed = result_embed)



async def setup(bot):
    bot.tree.add_command(Moderation(bot), guild=Config.mainServer)
    print('Group loaded')
