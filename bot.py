from discord.ext import commands

# Define bot
client = commands.Bot(command_prefix="크센아 ")
client.name = "AnnivBot"

# Register cog extensions
cogs = [
    "cogs.logger"
    ]

for cog in cogs:
    client.load_extension(cog)



