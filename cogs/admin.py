from discord import Member, Embed
from discord.ext.commands import Bot, Cog, Context, command, group
from .tools.groups import *
import logging


class AdminTools(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger("{}.{}".format(
            getattr(self.bot, "name") or "AnnivBot", self.__class__.__name__
            ))

        self.conf = getattr(self.bot, "conf_event")
        self.logger.info("Permisisons: {}".format(dict(self.conf)))

    @group(name="관리")
    async def _grp_admin(self, ctx: Context):
        if not ctx.invoked_subcommand:
            await ctx.send(ctx.author.mention + "\nSub-commands: \n```\n{}```".format(
                    "\n".join(["{} - {}".format(x.name, x.help) for x in self._grp_admin.commands])
                ))

    @_grp_admin.group(name="권한")
    async def _grp_admin_permissions(self, ctx):
        """디스코드 봇에 설정된 권한을 관리합니다."""

        if not ctx.invoked_subcommand:
            await ctx.send(ctx.author.mention + "\nSub-commands: \n```\n{}```".format(
                    "\n".join(["{} - {}".format(x.name, x.help) for x in self._grp_admin_permissions.commands])
                ))

    @_grp_admin_permissions.command(name="보기")
    async def view_permission(self, ctx, *, member: Member = None):
        """자신의 권한을 확인합니다. 만약 다른 사람을 언급하면, 그 사람의 권한을 확인합니다.
        필요한 권한: TeamCrescendo(타인의 권한 확인) or User(본인의 권한 확인)"""
        permission = await self.determine_permission(ctx.author)
        if member and permission() < TeamCrescendo():
            await ctx.send(ctx.author.mention + " 당신은 타인을 조회할 권한이 없습니다. (당신: {} < 필요: {})".format(
                permission.name, TeamCrescendo.name
                ))
            return

        member = member or ctx.author
        permission = await self.determine_permission(member)

        embed = Embed(title="{}의 권한".format(member))
        embed.add_field(name="권한", value=permission.name)
        embed.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=embed)

    async def determine_permission(self, user: Member):
        if user.id == (await self.bot.application_info()).owner.id:
            return Owner

        if {x.id for x in user.roles} & {int(x) for x in self.conf["admin_roles"].split(",")}:
            return TeamCrescendo

        return User


def setup(bot: Bot):
    bot.add_cog(AdminTools(bot))
