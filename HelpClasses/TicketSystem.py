import discord
from discord.ext import commands
from discord.ui import Button, View
from DataBase import DbWork

class MastersButton(View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Запросить помощь Мастера",style=discord.ButtonStyle.grey,emoji="📩")
    async def button_callback(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Создание тикета...", ephemeral=True)
        category = discord.utils.get(interaction.guild.categories, id=self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Categories"]["MasterTickets"])
        staff = interaction.channel.guild.get_role(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Roles"]["Staff"])

        overwrites = {
            category.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            staff: discord.PermissionOverwrite(read_messages=True)
        }
        ticket = await category.create_text_channel(f"Тикет {interaction.user.name}", overwrites=overwrites)
        await ticket.send("""Приветствуем! Пожалуйста заполните форму:
1) Тема вашего обращения (кратко)
2) Все необходимые ссылки (пост/анкета и т.д)
3) Детали ситуации.

Согласование и разбор вашей ситуации будет проходить в этом чате, старайтесь его не засорять.""")


class Ticket:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def load_tickets(self):
        await self._init_masters()

    async def _init_masters(self):
        channel = self.bot.get_channel(self.bot.SETTINGS["Guilds"]["MAIN_GUILD"]["Channels"]["MasterTickets"])
        async for message in channel.history(limit=None):
            await message.delete()

        description = "Приветствуем в службе ролевой поддержки!\nЗдесь вы можете запросить помощь Мастеров с любым вашим вопросом в РП!\nНажмите на кнопку внизу для подачи заявки - 📩"
        result_embed = discord.Embed(title="Вызов Мастера", description=description, colour=self.bot.SETTINGS["MAIN_COLOR"])
        button = MastersButton(self.bot)
        await channel.send(embed=result_embed, view=button)