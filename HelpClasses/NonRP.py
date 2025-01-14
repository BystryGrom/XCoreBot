import discord
from DataBase import DbWork
from time import time
from math import sqrt
from datetime import date, timedelta
from json import load

with open("./Resources/CONFIG.json", "r") as file:
    SETTINGS = load(file)

class Nrp:
    async def change_money(message_len: int, author: discord.Member, modificator: int = 1):
        new_money = (message_len * 0.001 + 0.05) * modificator
        user_money = DbWork.select("nrp", "money, series, date", f"WHERE userid = {author.id}")
        if not user_money:
            DbWork.insert("nrp", ["userid", "money", "series", "date"], [(author.id, new_money, 1, f"{date.today()}")])
            return

        yesterday = date.today() - timedelta(days=1)
        series = user_money[0][1]
        if user_money[0][2] == yesterday:
            series += 1
        elif user_money[0][2] != str(date.today()) and user_money[0][2] != str(yesterday):
            series = 1

        new_money = new_money * sqrt(series / 2)
        new_nickname = author.display_name + f" 🔥{series}."
        if len(author.display_name) >= 30 - series:
            new_nickname = author.display_name[:30 - len(str(series))] + f"🔥{series}."
        new_nickname = new_nickname.replace(f" 🔥{user_money[0][1] - 1}.", "")
        no_change = author.guild.get_role(1328382608970743899)
        if author.guild.id == SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"] and no_change not in author.roles:
            if author.display_name.find(f"🔥{series}.") == -1:
                await author.edit(nick=new_nickname)

        DbWork.update("nrp", f"money = {user_money[0][0] + new_money}, series = {series}, date = \"{date.today()}\"", f"userid = {author.id}")