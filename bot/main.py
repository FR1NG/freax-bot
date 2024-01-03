import discord
from discord.ext import commands
import os

token = os.environ.get('TOKEN')
intent = discord.Intents.default()
intent.members = True
intent.messages = True
intent.reactions = True
intent.guild_messages = True
intent.guild_reactions = True
intent.message_content = True
# intent.commands = True

bot = commands.Bot(command_prefix='/', intents=intent)

# tree = discord.app_commands.CommandTree(bot)

# @bot.command(name='mention', description='Mention everyone in the server')
@bot.tree.command(name='mention', description='Mention everyone in the server')
#@commands.has_permissions(mention_everyone=True)
async def mention(interaction: discord.Interaction):
    username = interaction.user.name
    role = discord.utils.get(interaction.guild.roles, name='FREAX')
    await interaction.response.send_message(f"{role.mention} {username} msad3 lina k***a")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run(token)

