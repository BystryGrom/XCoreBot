import discord
from discord.ext import commands
import asyncio
from CogsClasses import Banner, StaffStatistic


async def CycleStart(bot: commands.Bot):
    """

    ААЪХАХАХАХАХАХААХАХАХАХАХАХ

    БЕГИТЕ Я КОНЧЕНННЫЙ ХХАХАХААХАХА

    АХАХАХАХАХАХАХАХАХАХАХАХАХХ

    """

    while True:
        try:
            await Banner.change_banner(bot)
            await StaffStatistic.ankets(bot)
            await asyncio.sleep(360)
        except:
            pass
