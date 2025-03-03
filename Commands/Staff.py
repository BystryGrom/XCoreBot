import discord
from discord import app_commands as apc
from DataBase import DbWork
from datetime import datetime, timedelta
from typing import Literal
from time import time

class Development(apc.Group, name="персонал"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        self.staff_role = bot.get_guild(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"]).get_role(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Staff"])
        self.staff_members = bot.get_guild(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"]).get_channel(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["StaffMembers"])
        self.base_desc = "<t:{time}:f>\n> Серия рабочих дней: {series}\n\n- **Имя**: {name}\n- **Должность:** {vocation}\n- **Специализация:** {competence}\n- **От сотрудника:** {description}"

    @apc.command(name="установить_информацию")
    async def set_info(self, interaction: discord.Interaction, vocation: Literal["Ключевой Код", "Первый Сигнал", "Главный Ретранслятор", "Модератор", "Медиа", "Мастер", "Ивентолог", "Разработчик РП", "Анкетолог"], competence: str, name: str, description: str):
        """
        Устанавливает/Изменяет информацию о сотруднике Стаффа в определённом канале.

        :param vocation: Ваше официальное название должности.
        :param competence: Ваша специализация.
        :param name: То, как к вам стоит обращаться. Необязательно имя.
        :param description: Немного о себе!
        """
        await interaction.response.defer()
        staff_embed = discord.Embed(title=f"Информация про {interaction.user.name}", color=self.bot.SETTINGS["MAIN_COLOR"])

        if self.staff_role not in interaction.user.roles:
            await interaction.followup.send("Вы не являетесь членом персонала!")
            return

        info = DbWork.select("staff", "message", f"WHERE userid = {interaction.user.id}")
        if not info:
            staff_embed.description = self.base_desc.format(state="Отсутствует на смене", name=name, description=description, vocation=vocation, competence=competence, time = int(time()), series=1)
            message = await self.staff_members.send(embed=staff_embed)
            DbWork.insert("staff",
                          ["userid", "name", "description", "vocation", "competence", "message"],
                          [(interaction.user.id, name, description, vocation, competence, message.id)])
        else:
            staff_embed.description = self.base_desc.format(name=name, description=description, vocation=vocation, competence=competence, time = int(time()))
            message = await self.staff_members.fetch_message(info[0][1])
            await message.edit(embed=staff_embed)
            DbWork.update("staff",
                          f"name = \"{name}\", description = \"{description}\", vocation = \"{vocation}\", competence = \"{competence}\"",
                          f"userid = {interaction.user.id}")
        await interaction.followup.send("Информация изменена!")

async def setup(bot):
    bot.tree.add_command(Development(bot), guild=bot.dev_guild)
    bot.tree.add_command(Development(bot), guild=bot.main_guild)
    print('Group loaded')
