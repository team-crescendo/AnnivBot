from discord import Game, Message
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command, group
import logging


class Logger(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

        self.messages = [
            "∠Γ Team Crescendo is here!",
            "∠Γ Please visit https://discord.gg/t7QGJBe",
            "∠Γ {guild_count} Guilds, {user_count} Users",
            ]

    @Cog.listener()
    async def on_ready(self):
        self.logger.info("====== Bot info ======")
        self.logger.info("== Prefix: {} ".format(self.bot.command_prefix))
        self.logger.info("== User: {}(#{}) ".format(self.bot.user, self.bot.user.id))
        self.logger.info("== Owner: {owner}(#{owner.id}) ".format(owner=(await self.bot.application_info()).owner))

        # self.update_presence.start()

    @Cog.listener()
    async def on_message(self, msg: Message):
        self.logger.info(
            f"Guild: {msg.guild.name} | Channel: {msg.channel.name} | User: {msg.author.name} | Message: {msg.content}"
            )

    @command(name="test")
    async def test(self, ctx):
        await ctx.send("Yeah")

    @tasks.loop(seconds=5.0)
    async def update_presence(self):
        msg = self.messages[0]
        self.messages = self.messages[1:] + [msg]

        await self.bot.change_presence(
            activity=Game(msg.format(
                guild_count=len(self.bot.guilds),
                user_count=len(self.bot.users)
                ))
            )


def setup(bot: Bot):
    bot.add_cog(Logger(bot))
