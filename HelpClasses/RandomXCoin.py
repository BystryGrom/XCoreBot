import discord
from time import time
from DataBase import DbWork
from random import randint

class RandomXCoin:
    async def process(bot: discord.ext.commands.Bot):
        last_price = DbWork.select("xcoins_price", "price, time", "ORDER BY time DESC LIMIT 1")
        new_price = last_price[0][0]
        if randint(1, 100) == 1:
            new_price = last_price[0][0] * (randint(980, 1010) / 1000)
            DbWork.insert("xcoins_price", ["price", "time", "reason"], [(new_price, int(time()), "random")])

        miners = DbWork.select("xcoins", "userid, coins, miners", "WHERE miners != 0")
        miners_amount = 0
        for miner in miners: miners_amount += miner[2]

        coins = DbWork.select("xcoins", "coins")
        coins_amount = 0
        for coin in coins: coins_amount += coin[0]

        for miner in miners:
            coins = DbWork.select("xcoins", "coins", f"WHERE userid = {miner[0]}")
            DbWork.update("xcoins", f"coins = {coins[0][0] + 0.003 * miner[2]}", f"userid = {miner[0]}")
            new_price = new_price - 0.005 * miner[2] / coins_amount * new_price

        DbWork.insert("xcoins_price", ["price", "time", "reason"], [(new_price, int(time()), "miner")])
