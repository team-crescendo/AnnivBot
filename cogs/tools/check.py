from .groups import PermissionGroup, GroupPermissionError
from discord.ext.commands import check


def upper_permission(grp: PermissionGroup):
    async def predicate(ctx):
        perm = (await ctx.bot.get_cog("AdminTools").determine_permission(ctx.author))()
        if perm < grp:
            # return False
            raise GroupPermissionError(perm, grp)

        return True
    return check(predicate)
