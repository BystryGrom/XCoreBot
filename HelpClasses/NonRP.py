import discord
from DataBase import DbWork

class Nrp:
    async def change_money(message_len: int, author: discord.User, modificator: int = 1):
        new_money = (message_len * 0.001 + 0.05) * modificator
        user_money = DbWork.select("nrp", "money", f"WHERE userid = {author.id}")
        if not user_money:
            DbWork.insert("nrp", ["userid", "money"], [(author.id, new_money)])
            return
        DbWork.update("nrp", f"money = {user_money[0][0] + new_money}", f"userid = {author.id}")