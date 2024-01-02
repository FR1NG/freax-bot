
from dotenv import dotenv_values
import discord
from discord.ext import commands


config = dotenv_values('.env')


# uid = config['UID']
# key = config['KEY']
token = config.get('TOKEN') or ''

print(token)

intent = discord.Intents.default()
intent.members = True
intent.messages = True
intent.reactions = True
intent.guild_messages = True
intent.guild_reactions = True
intent.message_content = True
# intent.commands = True

bot = commands.Bot(command_prefix='!', intents=intent)

@bot.command(name='greet')
async def greet(ctx):
    await ctx.send("Hello! I'm a bot. How can I assist you?")

@bot.command(name='mention')
@commands.has_permissions(mention_everyone=True)
async def tageveryone(ctx, *, message=None):
    if not message:
        message = "Attention everyone!"
    await ctx.send(f"@everyone {ctx.author} msad3 lina k***a")

bot.run(token)
