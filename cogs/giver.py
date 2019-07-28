from discord import Message
from discord.ext.commands import Bot, Cog
import logging


class Giver(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

        self.conf = getattr(self.bot, "conf_event") or {}

        self._target_channels = [int(x) for x in self.conf.get("target_channels", "").split(",") if x]
        self.target_channels = []

        self._give_role = int(self.conf.get("target_role") or 0)
        self.give_role = None

    @Cog.listener()
    async def on_ready(self):
        for c in self._target_channels:
            channel = self.bot.get_channel(c)
            if channel:
                self.target_channels.append(channel)

        for guild in self.bot.guilds:
            if guild.get_role(self._give_role):
                self.give_role = guild.get_role(self._give_role)
                break

        self.logger.info("====== Giving Info ======\n" +
                         "== Target Channels: {}\n".format(", ".join(
                             "{}(#{})".format(x.name, x.id) for x in self.target_channels
                             )) +
                         "== Giving Role: {}".format("{role.name}(#{role.id})".format(role=self.give_role)
                                                     if self.give_role else "Not found"))

    @Cog.listener()
    async def on_message(self, msg: Message):
        if self.give_role and self.give_role.guild == msg.guild and  msg.channel in self.target_channels:
            await msg.author.edit(roles={*msg.author.roles} | {self.give_role})


def setup(bot: Bot):
    bot.add_cog(Giver(bot))
