from bot import AnnivBot as Bot
from discord import Member, Guild, Role
from discord.ext.commands import Cog
from time import time
import logging
import traceback


class ServerRolePair:
    server_id: int
    server: Guild
    role_id: int
    role: Role

    def __init__(self,
                server_id: int,
                role_id: int):
        self.server_id = server_id
        self.role_id = role_id

    def get_server(self, parent):
        self.server = parent.bot.get_guild(self.server_id)
        return self.server

    def get_role(self, bot: Bot):
        self.role = self.server.get_role(self.role_id)
        return self.role
    

class JoinGiver(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

        self.conf = getattr(self.bot, "conf_migung") or {}
        
        self.floor_6 = ServerRolePair(self.conf['6th_server'], self.conf['6th_role'])
        self.floor_9 = ServerRolePair(self.conf['9th_server'], self.conf['9th_role'])
        self.floor_10 = None
        self.feedback_channel = None

        self.floors = [int(x) for x in self.conf['floors']]

    @Cog.listener()
    async def on_ready(self):
        self.floor_6.get_server(self)
        self.floor_6.get_role(self)
        self.floor_9.get_server(self)
        self.floor_9.get_role(self)

        self.floor_10 = self.bot.get_guild(self.conf['master_server'])
        self.feedback_channel = self.floor_10.get_channel(self.conf['feedback_channel'])

        self.logger.info(
            " ====== Migung Join Role ====== \n" +
            " 6th : {pair.server.name}(#{pair.server.id}) -> giving {pair.role.name}(#{pair.role.id})\n".format(pair=self.floor_6) +
            " 9th : {pair.server.name}(#{pair.server.id}) -> giving {pair.role.name}(#{pair.role.id})\n".format(pair=self.floor_9)
        )

    @Cog.listener()
    async def on_member_join(self, member: Member):
        print(member.guild.id, type(member.guild.id))
        print(self.floors)
        if member.guild.id in self.floors:
            open("log.csv", "a", encoding="UTF-8").write("{},{},{}(#{})\n".format(time(), self.floors.index(member.guild.id)+1, member.name, member.id))


        if member.guild.id == self.floor_6.server_id:
            try:
                await member.edit(roles={*member.roles} | {self.floor_6.role})
                await self.feedback_channel.send("[*][6th] 역할 지급 -> {0.mention}(#{0.id})".format(member))
            except:
                b = traceback.format_exc()
                await self.feedback_channel.send("[!][6th] Catched exception on User {0.name}(#{0.id} {0.mention})\n```\n".format(member) + b + "\n```")

        elif member.guild.id == self.floor_9.server_id:
            try:
                await member.edit(roles={*member.roles} | {self.floor_9.role})
                await self.feedback_channel.send("[*][9th] 역할 지급 -> {0.mention}(#{0.id})".format(member))
            except:
                b = traceback.format_exc()
                await self.feedback_channel.send("[!][9th] Catched exception on User {0.name}(#{0.id} {0.mention})\n```\n".format(member) + b + "\n```")


def setup(bot: Bot):
    bot.add_cog(JoinGiver(bot))
