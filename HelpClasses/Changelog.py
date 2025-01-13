import discord
from datetime import datetime

class Changelog:
    async def auto_feedback(message: discord.Message):
        await message.add_reaction("📈")
        await message.add_reaction("📉")
        await message.create_thread(name=f"{datetime.today()}: {f'{datetime.now().time()}'[:8]}")