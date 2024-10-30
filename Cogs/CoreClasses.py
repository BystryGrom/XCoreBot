import discord
from discord.ext import commands
from DataBase import DbWork

class Nrp:
    async def changeMoney(message_len: int, author: discord.User, modificator: int = 1):
        new_money = (message_len * 0.002 + 0.15) * modificator
        user_money = DbWork.select("nrp", "money", f"WHERE userid = {author.id}")
        if not user_money:
            DbWork.insert("nrp", ["userid", "money"], [(author.id, new_money)])
            return
        DbWork.update("nrp", f"money = {user_money[0][0] + new_money}", f"userid = {author.id}")






async def setup(bot):
    pass
