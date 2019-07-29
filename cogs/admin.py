from bot import AnnivBot as Bot
from .tools.check import upper_permission
from .tools.groups import *
from discord import Member, Embed
from discord.ext.commands import Cog, Context, group
from psutil import boot_time
from datetime import timedelta, datetime
from time import time
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

        if {x.id for x in user.roles} & {*self.conf["admin_roles"]}:
            return TeamCrescendo

        return User

    @_grp_admin.group(name="정보")
    @upper_permission(TeamCrescendo())
    async def _grp_admin_info(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send(ctx.author.mention + "\nSub-commands: \n```\n{}```".format(
                    "\n".join(["{} - {}".format(x.name, x.help) for x in self._grp_admin.commands])
                ))

    @_grp_admin_info.command(name="조회")
    async def _grp_admin_info_view(self, ctx):
        embed = Embed(title="봇 상태")
        embed.add_field(
            name="서버 상태",
            value="\n".join(
                "**{}**: {}".format(k, v) for k, v in {
                    "Server Uptime": timedelta(seconds=time() - boot_time()),
                    "Bot Uptime": datetime.now() - ctx.bot.boot_time,
                    }.items()
                ),
            inline=False
            )
        embed.add_field(
            name="설정 정보",
            value="__**Bot**__\n\t" + "\n\t".join(
                "__{}__: {}".format(k, v) for k, v in self.bot.conf_bot.items()
                ) + "\n\n__**Event**__\n\t" + "\n\t".join(
                "__{}__: {}".format(k, v) for k, v in self.bot.conf_event.items()
                ) + "\n\n__**Roles**__\n\t" + "\n\t".join(
                "__{}__: {}".format(k, v) for k, v in {
                    "whitelist_guilds": ", ".join("{x.name}(#{x.id})".format(x=x) for x in self.bot.whitelist["guilds"]),
                    "whitelist_channels": ", ".join("<#{}>".format(x.id)for x in self.bot.whitelist["channels"]),
                    }.items()
                ),
            inline=False
            )
        embed.add_field(
            name="통계",
            value="\n".join(
                "**{}**: {}".format(k, v) for k, v in {
                    "Guilds": len(ctx.bot.guilds),
                    "Channels": len([*ctx.bot.get_all_channels()]),
                    "Members (Mutual)": len([*ctx.bot.get_all_members()]),
                    "Members (Non-Mutual)": len({x.id for x in ctx.bot.get_all_members()}),
                    }.items()
                ),
            inline=False
            )

        await ctx.send(embed=embed)

    @_grp_admin_info.error
    async def _grp_admin_info_error(self, ctx, error: GroupPermissionError):
        await ctx.send(ctx.author.mention + " " + error.make_message())

def setup(bot: Bot):
    bot.add_cog(AdminTools(bot))
