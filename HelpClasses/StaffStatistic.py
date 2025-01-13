import discord
from discord.ext import commands
from DataBase import DbWork

class StaffStatistic:
    async def ankets(bot: commands.Bot):
        ankets = DbWork.select("characters", "anketolog")

        amount = {}
        for anket in ankets:
            if amount.get(anket[0]) is None:
                amount[anket[0]] = 1
                continue
            new_amount = amount.get(anket[0]) + 1
            amount[anket[0]] = new_amount
        amount = sorted(amount.items(), key=lambda item: item[1])
        amount.reverse()
        amount = dict(amount)

        result = ""
        for id in amount.keys():
            if bot.get_user(id) is None: continue
            result += f"### `{bot.get_user(id).name}` - {amount.get(id)} анкет\n"

        result_embed = discord.Embed(description=result, colour=bot.SETTINGS["MAIN_COLOR"])
        channel = bot.get_channel(1316051926982332436)
        async for message in channel.history(limit=10000):
            await message.delete()
        await channel.send(embed = result_embed)