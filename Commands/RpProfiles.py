import time
import re
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
        name = re.sub("\'|\"|'", "", name)
        name = name.lower()
        rp_role = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['Roleplayer'])
        on_cheking = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['OnCheking'])

        profile = DbWork.select("characters", "name, au", f"WHERE userid = {user.id}")
        if len(profile) > 2:
            result_embed.description = f"Пользователь имеет двух зарегестрированных персонажей персонажа - {profile[0][0]} из {profile[0][1]} и {profile[1][0]} из {profile[1][1]}"
            await interaction.followup.send(embed = result_embed)
            return


        DbWork.insert("characters", ["userid", "name", "au", "channel", "anketolog"], [(user.id, name, au, interaction.channel.id, interaction.user.id)])
        result_embed.description = f"## Регистрация {user.mention}\n### - Имя: **{name}**\n### - Вселенная: **{au}**"
        await interaction.followup.send(embed = result_embed)
        if rp_role not in user.roles:
            await user.add_roles(rp_role)
        if on_cheking in user.roles:
            await user.remove_roles(on_cheking)
        await interaction.channel.edit(name=f"Принято - {name} {au}")
        registered_message = f"{user.mention} - {interaction.channel.mention}\n{name.capitalize()} из {au}"
        registered_channel = interaction.channel.guild.get_channel(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RegisteredCharacter"])
        await registered_channel.send(registered_message)


    @apc.command(name="снятие")
    async def exit_rp(self, interaction: discord.Interaction, name: str, user: discord.Member = None):
        """
        Снимает привязку к персонажу, выдавая роль "заблокирован".

        :param name: Имя персонажа, что будет снят.
        :param user: Пользователь, что будет снят. (Необязательный, только для Мастеров)
        """
        await interaction.response.defer()
        user = interaction.user if user is None else user
        name = name.lower()

        anketolog = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['Anketolog'])
        if anketolog not in interaction.user.roles and interaction.user != user:
            await interaction.followup.send("У вас нет прав на снятие других пользователей!")
            return

        result_embed = discord.Embed(colour=self.bot.SETTINGS["MAIN_COLOR"])

        profiles = DbWork.select("characters", "name, au", f"WHERE userid = {user.id} and name = '{name}'")
        if not profiles:
            await interaction.followup.send(f"{user.name} не имеет персонажа с именем {name}")
            return

        rp_role = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['Roleplayer'])
        if rp_role in user.roles:
            await user.remove_roles(rp_role)

        if len(profiles) == 1:
            rp_block = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['RpBlock'])
            if rp_block not in user.roles:
                await user.add_roles(rp_block)
            DbWork.insert("blocked", ["userid", "time"], [(user.id, time.time())])

        DbWork.delete("characters", f"userid = {user.id} AND name = '{name}'")

        registered_channel = interaction.channel.guild.get_channel(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RegisteredCharacter"])
        async for message in registered_channel.history(limit=None):
            if name in message.content and f"{user.id}" in message.content:
                await message.delete()

        result_embed.description = f"## Снятие {user.mention}\n - **{profiles[0][0]}** из **{profiles[0][1]}** выведен/а из рп."
        await interaction.followup.send(embed=result_embed)


    @apc.command(name="очистить_заблокированных")
    @apc.checks.has_permissions(manage_roles=True)
    async def clear_blocked(self, interaction: discord.Interaction):
        """
        Снимает роль "заблокирован" у зарегистрированных через бота пользователей
        """
        await interaction.response.send_message("Начало очистки...")
        blocked = DbWork.select("blocked")
        rp_block = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['RpBlock'])

        count = 0
        for userid in blocked:
            user = interaction.guild.get_member(userid[0])
            if user is not None:
                await user.remove_roles(rp_block)
            DbWork.delete("blocked", f"userid = {userid[0]}")
            count += 1

        await interaction.channel.send(f"Очистка завершена. Снято \"Заблокирован\": {count}")

async def setup(bot):
    bot.tree.add_command(RpProfiles(bot), guild=bot.main_guild)
    print('Group loaded')