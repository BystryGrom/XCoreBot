from discord.ext import commands, tasks
from HelpClasses.Banner import *
from HelpClasses.StaffStatistic import *

class Cycle:
    def __init__(self, bot):
        self.bot = bot
  
    @tasks.loop(seconds=300.0)
    async def FiveMinutes(self):
        """

        ААЪХАХАХАХАХАХААХАХАХАХАХАХ

        БЕГИТЕ Я КОНЧЕНННЫЙ ХХАХАХААХАХА

        АХАХАХАХАХАХАХАХАХАХАХАХАХХ

        """
        try:
            await Banner.change_banner(self.bot)
            await StaffStatistic.ankets(self.bot)
        except Exception as e:
            print(e)
