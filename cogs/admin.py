from discord.ext.commands import Bot, Cog, command, group
import logging


class Permission(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

        self.conf = getattr(self.bot, "conf_event")
        self.logger.info("Permisisons: {}".format(dict(self.conf)))


def setup(bot: Bot):
    bot.add_cog(Permission(bot))
