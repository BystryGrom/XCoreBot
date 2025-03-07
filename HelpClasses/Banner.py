import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import os

from datetime import datetime

class Banner:
    async def change_banner(bot: commands.Bot):
        main_guild = bot.get_guild(bot.SETTINGS["Guilds"]["MAIN_GUILD"]["guild_id"])
        users_count = main_guild.member_count
        voice_users = 0
        for voice in main_guild.voice_channels:
            voice_users += len(voice.members)

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

        best_user = bot.get_user(best[0])

        text_color = (255, 224, 46) if best_user.id in bot.SETTINGS["Premium"] else (255, 255, 255)

        banner = Image.open("./Resources/banner.png").convert("RGBA")
        await best_user.avatar.save("./Resources/avatar.png")
        big_avatar = Image.open("./Resources/avatar.png").convert("RGBA")
        mask = Image.open("./Resources/mask.png").convert("RGBA").resize((250, 250))
        small_avatar = big_avatar.resize((250, 250))
        username = best_user.name
        new_banner = banner.copy()
        draw = ImageDraw.Draw(new_banner)
        font = ImageFont.truetype("./Resources/Alphatermination.ttf", 150)
        draw.text((225, 425), str(users_count), (255, 255, 255), font=font)
        if voice_users < 10:
            draw.text((225, 585), str(voice_users), (255, 255, 255), font=font)
        else:
            draw.text((195, 585), str(voice_users), (255, 255, 255), font=font)
        user_font = ImageFont.truetype("./Resources/Alphatermination.ttf", 250 - (len(username) * 7.4))
        draw.text((350, 950 + len(username) * 4), username, text_color, font=user_font)
        new_banner.paste(small_avatar, (60, 950), mask)
        new_banner.save("./new_banner.gif")
        with open("./new_banner.gif", "rb") as file:
            await main_guild.edit(banner=file.read())