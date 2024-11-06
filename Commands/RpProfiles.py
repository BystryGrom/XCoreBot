import discord
from discord import app_commands as apc
from DataBase import DbWork

class RpProfiles(apc.Group, name="анкеты"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="регистрация")
    async def registration(self, interaction: discord.Interaction, user: discord.Member, name: str, au: str):
        """
        Регистрирует персонажа Пользователя.

        :param user: Пользователь, что будет зарегистрирован.
        :param name: Имя персонажа.
        :param au: Вселенная персонажа
        """
        result_embed = discord.Embed(title=f"Регистрация {user.mention}", colour=self.bot.SETTINGS["MAIN_COLOR"])

        profile = DbWork.select("rp_profiles", "name, au", f"WHERE userid = {user.id}")
        if profile:
            result_embed.description = f"Пользователь имеет зарегистрированного персонажа - {profile[0][0]} из {profile[0][1]}"
            await interaction.response.send_message(embed = result_embed)
            return

        DbWork.insert("rp_profiles", ["userid", "name", "au", "channel"], [(user.id, name, au, interaction.channel.id)])
        result_embed.description = f"### - Имя: **{name}**\n### - Вселенная: **{au}**"
        await interaction.response.send_message(embed = result_embed)

        # Бля доделай потом, заебал


    @apc.command(name="снятие")
    async def exit_rp(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Снимает привязку к персонажу, выдавая роль "заблокирован".

        :param user: Пользователь, что будет снят. (Необязательный, только для Мастеров)
        """
        role = user.guild.get_role(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Anketolog"])
        if user != interaction.user and role not in interaction.user.roles:
            await interaction.response.send_message("У вас нет прав на снятие других участников", ephemeral = True)
            return

        # Бля доделай потом, заебал


async def setup(bot):
    bot.tree.add_command(RpProfiles(bot), guild=bot.dev_guild)
    print('Group loaded')