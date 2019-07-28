from discord.ext import commands
from discord.ext.commands import ExtensionError
from configparser import ConfigParser
import logging
import traceback


# Load configuration
conf = ConfigParser()
conf.read("settings.ini", encoding="UTF-8")
Bot = conf["Bot"]
Event = conf["Event"]

# Load logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Bot["Name"])

# Define bot
client = commands.Bot(command_prefix=Bot["Prefix"])
client.name = Bot["Name"]
client.conf_event = Event

# Register cog extensions
cogs = [
    "cogs.logger",
    "cogs.admin"
    ]

logger.info("Loading {} extensions".format(len(cogs)))
for cog in cogs:
    try:
        client.load_extension(cog)

    except ExtensionError as ex:
        logger.warning("Error {} was occured when loading cog extension '{}'\n{}".format(
            ex.__class__.__name__, cog, traceback.format_exc()
            ))
logger.info("Loaded {} extensions".format(len(client.extensions)))


client.run(Bot["Token"])
