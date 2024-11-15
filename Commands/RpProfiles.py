import discord
from discord import app_commands as apc
from DataBase import DbWork

class RpProfiles(apc.Group, name="анкеты"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="регистрация")
    @apc.checks.has_permissions(manage_roles=True)
    async def registration(self, interaction: discord.Interaction, user: discord.Member, name: str, au: str):
        """
        Регистрирует персонажа Пользователя.

        :param user: Пользователь, что будет зарегистрирован.
        :param name: Имя персонажа.
        :param au: Вселенная персонажа
        """
        await interaction.response.defer()
        result_embed = discord.Embed(colour=self.bot.SETTINGS["MAIN_COLOR"])

        profile = DbWork.select("characters", "name, au", f"WHERE userid = {user.id}")
        if profile:
            result_embed.description = f"Пользователь имеет зарегистрированного персонажа - {profile[0][0]} из {profile[0][1]}"
            await interaction.followup.send(embed = result_embed)
            return

        DbWork.insert("characters", ["userid", "name", "au", "channel", "anketolog"], [(user.id, name, au, interaction.channel.id, interaction.user.id)])
        result_embed.description = f"## Регистрация {user.mention}\n### - Имя: **{name}**\n### - Вселенная: **{au}**"
        await interaction.followup.send(embed = result_embed)

        registered_message = f"{user.mention} - {interaction.channel.mention}\n{name.capitalize()} из {au}"
        registered_channel = interaction.channel.guild.get_channel(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RegisteredCharacter"])
        await registered_channel.send(registered_message)


    @apc.command(name="снятие")
    async def exit_rp(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Снимает привязку к персонажу, выдавая роль "заблокирован".

        :param user: Пользователь, что будет снят. (Необязательный, только для Мастеров)
        """

        # Бля доделай потом, заебал


async def setup(bot):
    bot.tree.add_command(RpProfiles(bot), guild=bot.main_guild)
    print('Group loaded')