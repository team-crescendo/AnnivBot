__all__ = ["Owner", "TeamCrescendo", "User", "Restricted"]


class PermissionGroup:
    name = ""
    rank = ""

    # lt, le, gt, ge is reversed for rank concept
    @classmethod
    def __lt__(cls, other):
        return cls.rank > other.rank

    @classmethod
    def __le__(cls, other):
        return cls.rank >= other.rank

    @classmethod
    def __gt__(cls, other):
        return cls.rank < other.rank

    @classmethod
    def __ge__(cls, other):
        return cls.rank <= other.rank

    @classmethod
    def __eq__(cls, other):
        return cls.rank == other.rank

    @classmethod
    def __ne__(cls, other):
        return cls.rank != other.rank


class Owner(PermissionGroup):
    name = "Owner"
    rank = 0


class TeamCrescendo(PermissionGroup):
    name = "팀 크레센도"
    rank = 1


class User(PermissionGroup):
    name = "유저"
    rank = 10


class Restricted(PermissionGroup):
    name = "제한된 유저"
    rank = 90
