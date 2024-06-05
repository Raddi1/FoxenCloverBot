import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os


intents = disnake.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"), intents=intents)

@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} запущений!")

class ApplicationModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Твій нік в Minecraft",
                placeholder="Введи свій нік в Minecraft",
                custom_id="minecraft_nickname",
                style=disnake.TextInputStyle.short,
                min_length=3,
                max_length=30,
            ),
            disnake.ui.TextInput(
                label="Плани на сервері?",
                placeholder="Розкажи про свої плани на сервері",
                custom_id="plans",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label="Розкажи про себе",
                placeholder="Розкажи трохи про себе",
                custom_id="about",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label="Попередні проєкти?",
                placeholder="Розкажи про проєкти, на яких ти грав",
                custom_id="previous_projects",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=500,
            ),
        ]
        super().__init__(title="Форма заявки", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        minecraft_nickname = inter.text_values["minecraft_nickname"]
        plans = inter.text_values["plans"]
        about = inter.text_values["about"]
        previous_projects = inter.text_values["previous_projects"]

        channel = bot.get_channel(1247648187880308868)  # Замініть на ідентифікатор каналу для заявок

        embed = disnake.Embed(title="Нова заявка!", color=disnake.Color.blue())
        embed.add_field(name="Твій нік в Minecraft", value=minecraft_nickname, inline=False)
        embed.add_field(name="Плани та заняття на сервері", value=plans, inline=False)
        embed.add_field(name="Про себе", value=about, inline=False)
        embed.add_field(name="Проєкти, на яких грав раніше", value=previous_projects, inline=False)
        embed.set_footer(text=f"Від {inter.author.display_name}")

        await channel.send(embed=embed, components=[
            disnake.ui.Button(label="Прийняти", custom_id="accept_button", style=disnake.ButtonStyle.success),
            disnake.ui.Button(label="Відхилити", custom_id="reject_button", style=disnake.ButtonStyle.danger)
        ])

@bot.slash_command(description="Відкриває форму заявки")
async def create(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message("Для початку гри нажми на кнопку нижче", components=[
        disnake.ui.Button(label="Подати заявку", custom_id="application_button", style=disnake.ButtonStyle.primary)
    ], ephemeral=True)


@bot.listen("on_button_click")
async def on_button_click(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "application_button":
        if inter.author.guild_permissions.administrator:
            await inter.response.send_modal(modal=ApplicationModal())
        else:
            await inter.response.send_message("У вас немає прав для перегляду цієї форми.", ephemeral=True)
    elif inter.component.custom_id == "accept_button":
        channel_id = 1247647317402845279  # Замініть на ідентифікатор каналу, куди ви хочете відправити результат
        channel = bot.get_channel(channel_id)
        user = inter.author  # Отримання користувача
        user_mention = user.mention  # Отримання згадки про користувача
        
        # Створення embed з помаранчевим кольором
        embed = disnake.Embed(title="Заявка прийнята!", color=disnake.Color.green())
        embed.set_author(name=str(user), icon_url=user.avatar.url)
        
        await channel.send(content=user_mention, embed=embed)
        await inter.response.send_message("Заявка прийнята!")

    elif inter.component.custom_id == "reject_button":
        channel_id = 1247647317402845279  # Замініть на ідентифікатор каналу, куди ви хочете відправити результат
        channel = bot.get_channel(channel_id)
        user = inter.author if inter.author else None
        user_mention = user.mention  # Отримання згадки про користувача
    
        # Створення embed з червоним кольором
        embed = disnake.Embed(title="Заявка відхилена!", color=disnake.Color.red())
        embed.set_author(name=str(user), icon_url=user.avatar.url)
    
        await channel.send(content=f"{user_mention} твоя заявка була відхилена!", embed=embed)
        await inter.response.send_message("Заявка відхилена!")


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
