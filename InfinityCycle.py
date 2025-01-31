from discord.ext import commands
import asyncio
from HelpClasses.Banner import *
from HelpClasses.StaffStatistic import *


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
            await asyncio.sleep(300)
        except Exception as e:
            print(e)
            await asyncio.sleep(10)
