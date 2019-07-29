from bot import AnnivBot
from settings import Setting
from discord.ext.commands import ExtensionError
import logging
import traceback


# Load configuration
conf = Setting()

# Load logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(conf.conf["Bot"]["name"])

# Define bot
client = AnnivBot(conf)

# Register cog extensions
cogs = [
    "cogs.logger",
    "cogs.admin",
    "cogs.giver",
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
logger.info("Loaded {} commands: {}".format(
    len(client.commands), [x.name for x in client.commands]
    ))


client.kick()
