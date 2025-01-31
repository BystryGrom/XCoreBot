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
        self.base_desc = "> Состояние: **{state} - <t:{time}:f>**\n> Серия рабочих дней: {series}\n\n- **Имя**: {name}\n- **Должность:** {vocation}\n- **Специализация:** {competence}\n- **От сотрудника:** {description}"

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
        staff_embed = discord.Embed(title=f"Информация про {interaction.user.global_name}", color=self.bot.SETTINGS["MAIN_COLOR"])

        if self.staff_role not in interaction.user.roles:
            await interaction.followup.send("Вы не являетесь членом персонала!")
            return

        info = DbWork.select("staff", "state, message", f"WHERE userid = {interaction.user.id}")
        series = DbWork.select("work_series", "series", f"WHERE userid = {interaction.user.id}")
        if not info:
            staff_embed.description = self.base_desc.format(state="Отсутствует на смене", name=name, description=description, vocation=vocation, competence=competence, time = int(time()), series=1)
            message = await self.staff_members.send(embed=staff_embed)
            DbWork.insert("staff",
                          ["userid", "name", "description", "vocation", "competence", "state", "message"],
                          [(interaction.user.id, name, description, vocation, competence, "Отсутствует на смене", message.id)])
            DbWork.insert("work_series", ["userid", "series", "date"], [(interaction.user.id, 1, datetime.today())])
        else:
            staff_embed.description = self.base_desc.format(state=info[0][0], name=name, description=description, vocation=vocation, competence=competence, time = int(time()), series=series[0][0])
            message = await self.staff_members.fetch_message(info[0][1])
            await message.edit(embed=staff_embed)
            DbWork.update("staff",
                          f"name = \"{name}\", description = \"{description}\", vocation = \"{vocation}\", competence = \"{competence}\"",
                          f"userid = {interaction.user.id}")
        await interaction.followup.send("Информация изменена!")

    @apc.command(name="изменить_состояние")
    async def change_state(self, interaction: discord.Interaction, is_holiday: bool = False):
        """
        Изменяет состояние сотрудника. Обычное использование инвертирует Отсутствие на Присутствие и наоборот.

        :param is_holiday: Опциональный параметр, указывающий на бытие в отпуске.
        """
        await interaction.response.defer()
        result_embed = discord.Embed(title=f"Изменение состояния",
                                    color=self.bot.SETTINGS["MAIN_COLOR"])

        if self.staff_role not in interaction.user.roles:
            await interaction.followup.send("Вы не являетесь членом персонала!")
            return

        info = DbWork.select("staff", "name, description, vocation, competence, state, message", f"WHERE userid = {interaction.user.id}")
        if not info:
            await interaction.followup.send("У вас не зарегистрирована информация о себе!")
            return

        series = DbWork.select("work_series", "series, date", f"WHERE userid = {interaction.user.id}")

        match info[0][4]:
            case "Отсутствует на смене":
                state = "На смене"
                if series[0][1] == datetime.today() - timedelta(days=1):
                    DbWork.update("work_series", f"series = {series[0][0] + 1}, date = \"{datetime.today()}\"", f"userid = {interaction.user.id}")
                elif series[0][1] != datetime.today():
                    DbWork.update("work_series", f"series = 1, date = \"{datetime.today()}\"",
                                  f"userid = {interaction.user.id}")
            case "На смене": state ="Отсутствует на смене"
            case "В отпуске": state = "На смене"
        if is_holiday: state = "В отпуске"

        staff_embed = discord.Embed(title=f"Информация про {interaction.user.global_name}",
                                    description= self.base_desc.format(state=state, name=info[0][0], description=info[0][1],vocation=info[0][2], competence=info[0][3], time=int(time()), series=series[0][0]),
                                    color=self.bot.SETTINGS["MAIN_COLOR"])

        message = await self.staff_members.fetch_message(info[0][5])
        await message.edit(embed=staff_embed)
        DbWork.update("staff", f"state = \"{state}\"", f"userid = {interaction.user.id}")

        result_embed.description = f"Статус успешно установлен на \"{state}\""
        await interaction.followup.send(embed=result_embed)

async def setup(bot):
    bot.tree.add_command(Development(bot), guild=bot.dev_guild)
    bot.tree.add_command(Development(bot), guild=bot.main_guild)
    print('Group loaded')
