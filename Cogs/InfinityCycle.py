import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import asyncio


async def setup(bot: commands.Bot):
    """

    ААЪХАХАХАХАХАХААХАХАХАХАХАХ

    БЕГИТЕ Я КОНЧЕНННЫЙ ХХАХАХААХАХА

    АХАХАХАХАХАХАХАХАХАХАХАХАХХ

    """

    main_guild = bot.get_guild(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"])
    while True:
        users_count = main_guild.member_count
        voice_users = 0
        for voice in main_guild.voice_channels:
            for member in voice.members:
                voice_users += 1

        general = main_guild.get_channel(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["General"])
        now = datetime.now()
        if now != 0:
            now = now.replace(hour=now.hour - 1)
        activities = []
        async for message in general.history(after=now):
            activities.append(message.author.id)
        unique_users = set(activities)
        best = (0, 0)
        for user in unique_users:
            if activities.count(user) > best[1]:
                best = (user, activities.count(user))

        print(activities)
        print(best)
        best_user = bot.get_user(best[0])

        banner = Image.open("./Resources/banner.gif").convert("RGB")
        await best_user.avatar.save("./Resources/avatar.png")
        big_avatar = Image.open("./Resources/avatar.png").convert("RGB")
        mask = Image.open("./Resources/mask.png").convert("RGBA")
        small_avatar = big_avatar.resize((100, 100))
        username = best_user.name
        new_banner = banner.copy()
        draw = ImageDraw.Draw(new_banner)
        font = ImageFont.truetype("./Resources/Alphatermination.ttf", 50)
        draw.text((85, 105), str(users_count), (255, 255, 255), font=font)
        if voice_users < 10:
            draw.text((85, 165), str(voice_users), (255, 255, 255), font=font)
        else:
            draw.text((75, 165), str(voice_users), (255, 255, 255), font=font)
        user_font = ImageFont.truetype("./Resources/Alphatermination.ttf", 70 - (len(username) * 2))
        draw.text((165, 340 + len(username)), username, (255, 255, 255), font=user_font)
        new_banner.paste(small_avatar, (40, 325), mask)
        new_banner.save("./new_banner.gif")
        with open("./new_banner.gif", "rb") as file:
            await main_guild.edit(banner=file.read())


        await asyncio.sleep(360)
