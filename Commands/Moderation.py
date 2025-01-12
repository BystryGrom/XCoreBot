import discord
from discord import app_commands as apc
from DataBase import DbWork


class Moderation(apc.Group, name="мод"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="варн")
    @apc.checks.has_permissions(ban_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, grade: int, reason: str):
        """
        Выдаёт предупреждение Пользователю.

        :param user: Пользователь, что получит предупреждение.
        :param grade: Количество баллов предупреждения.
        :param reason: Причина предупреждения.
        """

        if grade < 1:
            await interaction.response.send_message("Кол-во баллов не может быть отрицательным.", ephemeral = True)
            return

        await interaction.response.defer()

        warns = DbWork.select("warns", "id, grade", f"WHERE userid = {user.id} ORDER BY id")
        id = 1 if not warns else warns[-1][0] + 1

        DbWork.insert("warns",
                      ["id", "userid", "grade", "reason"],
                      [(id, user.id, grade, reason)])

        result_grade = grade
        for warn in warns: result_grade += warn[1]

        result_embed = discord.Embed(title="Выдача Варна", description=f"> Варн № {id} пользователя {user.mention}\n- Вес: {grade}\n- Причина: {reason}", color=self.bot.SETTINGS["MAIN_COLOR"])

        if result_grade >= 10:
            result_embed.description = result_embed.description + "\n\n### - Превышен лимит баллов. Выдан бан."
            await user.send("Вы были забанены на сервере Alpha Timeline по достижению десяти баллов")
            await user.ban(reason=reason)

        await interaction.followup.send(f"<@{user.id}>", embed = result_embed)

    @apc.command(name="удалить_варн")
    @apc.checks.has_permissions(ban_members=True)
    async def remove_warn(self, interaction: discord.Interaction, user: discord.User, id: int):
        """
        Удаляет предупреждение Пользователя.

        :param user: Пользователь, чей варн будет удален.
        :param id: Айди варна пользователя.
        """
        warn = DbWork.select("warns", "grade, reason", f"WHERE id = {id} AND userid = {user.id}")
        if not warn:
            await interaction.response.send_message("Warn was not found.", ephemeral = True)
            return
        DbWork.delete("warns", f"id = {id} AND userid = {user.id}")
        result_embed = discord.Embed(title="Удаление варна", description=f"> Удалён варн № {id} пользователя {user.mention}\n- Вес: {warn[0][0]}\n- Причина: {warn[0][1]}", color=self.bot.SETTINGS["MAIN_COLOR"])
        await interaction.response.send_message(embed = result_embed)


    @apc.command(name="варны")
    async def warns(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Отображает количество варнов Пользователя.

        :param user: Пользователь, варны которого отобразятся. (Необязательный, по умолчанию - вы)
        """
        await interaction.response.defer()
        user = interaction.user if user is None else user

        result_embed = discord.Embed(title=f"Варны {user.display_name}", color=self.bot.SETTINGS["MAIN_COLOR"])
        warns = DbWork.select("warns", "id, grade, reason", f"WHERE userid = {user.id}")
        if not warns:
            result_embed.description = "**○ ○ ○ ○ ○ ○ ○ ○ ○ ○**"
            await interaction.followup.send(embed = result_embed)
            return

        result_grade = 0
        text_warns = ""
        for warn in warns:
            result_grade += warn[1]
            text_warns += f"\n№ {warn[0]} - {' ●' * warn[1]}: {warn[2]}"
        result_embed.description=f"# {' **●**' * result_grade}{' **○**' * (10 - result_grade)}\n" + text_warns

        await interaction.followup.send(embed = result_embed)



async def setup(bot):
    bot.tree.add_command(Moderation(bot), guild=bot.main_guild)
    print('Group loaded')
