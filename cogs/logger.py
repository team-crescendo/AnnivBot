from discord.ext.commands import Bot, Cog, command, group
import logging


class Logger(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

    @Cog.listener()
    async def on_ready(self):
        self.logger.info("Bot Initialized with Account '{}'(#{})".format(self.bot.user, self.bot.user.id))


def setup(bot: Bot):
    bot.add_cog(Logger(bot))
