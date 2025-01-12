import discord
from discord import app_commands as apc
from DataBase import DbWork


class Fun(apc.Group, name="фан"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command(name="создать_тег")
    async def create_tag(self, interaction: discord.Interaction, tag: str, value: str):
        """
        Создаёт тег.

        :param tag: То, что должен написать пользователь
        :param value: То, что выдаст пользователю бот
        """
        await interaction.response.defer()
        Embed = discord.Embed(description=f"Тег {tag.lower()} был создан!", colour=self.bot.SETTINGS["MAIN_COLOR"])

        current_tag = DbWork.select("tags", "author", f"WHERE tag = '{tag}'")
        if current_tag:
            Embed.description = f"Тег {tag.lower()} уже создан <@{current_tag[0][0]}>."
            await interaction.followup.send(embed = Embed)
            return
        if len(tag) > 12:
            Embed.description = f"Длина тега не может превышать 12 символов."
            await interaction.followup.send(embed=Embed)
            return
        DbWork.insert("tags", ["tag", "value", "author"], [(tag.lower(), value, interaction.user.id)])

        await interaction.followup.send(embed = Embed)

    @apc.command(name="удалить_тег")
    async def delete_tag(self, interaction: discord.Interaction, tag: str):
        """
        Удаляет тег. Если вы не создатель тега, вам не удастся его удалить.

        :param tag: Тег, что будет удален.
        """
        await interaction.response.defer()
        Embed = discord.Embed(description=f"Тег {tag.lower()} был удален!", colour=self.bot.SETTINGS["MAIN_COLOR"])

        current_tag = DbWork.select("tags", "author", f"WHERE tag = '{tag}'")
        if not current_tag:
            Embed.description = f"Тега {tag.lower()} не существует."
            await interaction.followup.send(embed=Embed)
            return
        if current_tag[0][0] == interaction.user.id or interaction.user.id == 875620156410298379:
            DbWork.delete("tags", f"tag = '{tag}'")
            await interaction.followup.send(embed=Embed)

    @apc.command(name="оставить_пасхалко")
    async def message_to_santa(self, interaction: discord.Interaction, message: str):
        await interaction.channel.guild.get_channel(1318146055094931466).send(f"From {interaction.user.mention}:\n{message}")
        await interaction.response.send_message("Пасхалко оставлена", ephemeral=True)

async def setup(bot):
    bot.tree.add_command(Fun(bot), guild=bot.main_guild)
    print('Group loaded')