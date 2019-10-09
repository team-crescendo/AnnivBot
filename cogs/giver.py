from bot import AnnivBot as Bot
from discord import TextChannel, Message
from discord.ext.commands import Cog
from string import ascii_letters, digits
import random
import logging
import traceback


class Giver(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

        self.conf = getattr(self.bot, "conf_event") or {}

        self._target_channels = self.conf.get("target_channels")
        self.target_channels = []

        self._give_role = int(self.conf.get("target_role") or 0)
        self.give_role = None

    @Cog.listener()
    async def on_ready(self):
        if not isinstance(self._target_channels, list):
            self._target_channels = [self._target_channels]

        for c in self._target_channels:
            channel = self.bot.get_channel(c)
            print("Browsing", c)
            if channel:
                print("Adding", channel)
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
        try:
            if self.give_role and self.give_role.guild == msg.guild and \
                    self.give_role not in msg.author.roles and \
                    (msg.channel in self.target_channels or msg.channel.id in self._target_channels):
                await msg.author.edit(roles={*msg.author.roles} | {self.give_role})
                await msg.add_reaction("⭕")
        except:
            try:
                tb = traceback.format_exc()
                report_name = "".join(random.choice(ascii_letters + digits) for i in range(8))
                open(report_name + ".log", "w", encoding="UTF-8").write(tb)

                report_channel: TextChannel = self.bot.get_channel(612249837848756224)
                await report_channel.send("역할 지급 중 오류 발생 ({})\n```py\n{}\n```".format(report_name, tb))
                await msg.add_reaction("❌")
            except:
                print("Error on message `{},,`({}) from `{}` in `{}({})\n\n=>{}`'".format(
                    msg.content[:10], msg.id, msg.author.mention, msg.guild.name, msg.channel.id, tb))


def setup(bot: Bot):
    bot.add_cog(Giver(bot))
