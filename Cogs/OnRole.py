from discord.ext import commands
import discord

class OnRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        @bot.event
        async def on_member_update(before: discord.Member, after: discord.Member):
            if before.roles != after.roles:
                block_role = before.guild.get_role(self.bot.SETTINGS['Guilds']['MAIN_GUILD']['Roles']['RpBlock'])
                async for entry in self.bot.get_guild(self.bot.main_guild.id).audit_logs(action=discord.AuditLogAction.member_role_update):
                    if entry.target.id == after.id:
                        gandon = entry.user
                        break

                if gandon.id != self.bot.user.id:
                    if block_role in before.roles and block_role not in after.roles:
                        await self.bot.get_guild(self.bot.dev_guild.id).get_channel(1348295494396411985).send(f"ЭТОГО НА ДНО! {gandon.mention} СНЯЛ РОЛЬ БЛОКА ДЛЯ {after.mention}! <@&1230793081960267787>")
                    elif block_role not in before.roles and block_role in after.roles:
                        await self.bot.get_guild(self.bot.dev_guild.id).get_channel(1348295494396411985).send(f"ЭТОГО НА ДНО! {gandon.mention} ДОБАВИЛ РОЛЬ БЛОКА ДЛЯ {after.mention}! <@&1230793081960267787>")

async def setup(bot):
    await bot.add_cog(OnRole(bot))
    print('Cock\'s loaded')
