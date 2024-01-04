import discord
from discord.ext import commands
import os

token = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
intents.guild_messages = True
intents.guild_reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

allowed_mentions = discord.AllowedMentions(roles=True)

@bot.tree.command(name='mention', description='Mention a role in the server')
async def mention(interaction: discord.Interaction, role_name: str = "freax"):
    role = discord.utils.get(interaction.guild.roles, name=role_name)

    if role:
        if role.mentionable and interaction.channel.permissions_for(interaction.guild.me).mention_everyone:
            await interaction.response.send_message(f"{role.mention} fri3 lk**r by {interaction.user.display_name}", allowed_mentions=allowed_mentions)
            await interaction.response.send_message("had l9lawi khaso permissions.")
    else:
        await interaction.response.send_message("Role not found.")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


bot.run(token)
