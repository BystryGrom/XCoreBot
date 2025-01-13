import discord
from DataBase import DbWork
from time import time
from math import sqrt
from datetime import date, timedelta

class Nrp:
    async def change_money(message_len: int, author: discord.Member, modificator: int = 1):
        new_money = (message_len * 0.001 + 0.05) * modificator
        user_money = DbWork.select("nrp", "money, series, date", f"WHERE userid = {author.id}")
        if not user_money:
            DbWork.insert("nrp", ["userid", "money", "series", "date"], [(author.id, new_money, int(time()), date.today())])
            return

        yesterday = date.today() - timedelta(days=1)
        series = user_money[0][1]
        if user_money[0][2] == yesterday:
            new_money = new_money * sqrt(series / 2)
            series += 1

        new_nickname = author.display_name + f" 🔥{series}."
        if len(author.display_name) >= 30 - series:
            new_nickname = author.display_name[:30 - len(str(series))] + f"🔥{series}."
        if author.display_name.find(f"🔥{series}.") == -1:
            await author.edit(nick=new_nickname)

        elif user_money[0][2] != date.today(): series = 1
        DbWork.update("nrp", f"money = {user_money[0][0] + new_money}, series = {series}, date = \"{date.today()}\"", f"userid = {author.id}")