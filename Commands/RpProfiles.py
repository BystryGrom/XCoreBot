import time

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

        rp_role = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['Roleplayer'])
        on_cheking = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['OnCheking'])

        profile = DbWork.select("characters", "name, au", f"WHERE userid = {user.id}")
        if profile:
            result_embed.description = f"Пользователь имеет зарегистрированного персонажа - {profile[0][0]} из {profile[0][1]}"
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
    async def exit_rp(self, interaction: discord.Interaction):
        """
        Снимает привязку к персонажу, выдавая роль "заблокирован".

        :param user: Пользователь, что будет снят. (Необязательный, только для Мастеров)
        """
        await interaction.response.defer()
        result_embed = discord.Embed(colour=self.bot.SETTINGS["MAIN_COLOR"])

        profile = DbWork.select("characters", "name, au", f"WHERE userid = {interaction.user.id}")
        if not profile:
            await interaction.followup.send("Вы не имеете зарегистрированного персонажа")
            return

        rp_role = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['Roleplayer'])
        if rp_role in interaction.user.roles:
            await interaction.user.remove_roles(rp_role)

        rp_block = interaction.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['RpBlock'])
        if rp_block not in interaction.user.roles:
            await interaction.user.add_roles(rp_block)

        DbWork.delete("characters", f"userid = {interaction.user.id}")
        DbWork.insert("blocked", ["userid", "time"], [(interaction.user.id, time.time())])

        registered_channel = interaction.channel.guild.get_channel(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["RegisteredCharacter"])
        async for message in registered_channel.history(limit=None):
            if f"{interaction.user.id}" in message.content:
                await message.delete()

        result_embed.description = f"## Снятие {interaction.user.mention}\n - **{profile[0][0]}** из **{profile[0][1]}** выведен/а из рп."
        await interaction.followup.send(embed=result_embed)


    @apc.command(name="очистить_заблокированных")
    @apc.checks.has_permissions(manage_roles=True)
    async def clear_blocked(self, interaction: discord.Interaction):
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