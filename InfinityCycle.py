from discord.ext import commands, tasks
from HelpClasses.Banner import *
from HelpClasses.StaffStatistic import *

@tasks.loop(seconds=300.0)
async def CycleStart(bot: commands.Bot):
    """

    ААЪХАХАХАХАХАХААХАХАХАХАХАХ

    БЕГИТЕ Я КОНЧЕНННЫЙ ХХАХАХААХАХА

    АХАХАХАХАХАХАХАХАХАХАХАХАХХ

    """
    try:
        await Banner.change_banner(bot)
        await StaffStatistic.ankets(bot)
    except Exception as e:
        print(e)
