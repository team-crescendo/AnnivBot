from discord.ext.commands import Bot
from settings import Setting


class AnnivBot(Bot):
    def __init__(self, conf: Setting):
        self.conf = conf.conf

        self._a_bot = self.conf.get("Bot", {})
        self._a_token = self._a_bot.get("token")
        self._a_name = self._a_bot.get("name", self.__class__.__name__)
        self._a_command_prefix = self._a_bot.get("prefix", ";")
        self._a_command_prefix += " " if self._a_command_prefix[-1] != " " else ""

        self._a_event = self.conf.get("Event", {})

        self.whitelist = {
            "channels": self._a_bot.get("whitelist_channels", []),
            "guilds": self._a_bot.get("whitelist_guilds", []),
            }

        super().__init__(command_prefix=self._a_command_prefix)

    # Property for prior structure support (Rewriting)
    @property
    def conf_bot(self):
        return self._a_bot

    # Property for prior structure support (Rewriting)
    @property
    def conf_event(self):
        return self._a_event

    # Property for prior structure support (Rewriting)
    @property
    def name(self):
        return self._a_name

    def kick(self):
        self.run(self._a_token)
