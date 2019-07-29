from discord.ext.commands import CheckFailure

__all__ = ["PermissionGroup", "Owner", "TeamCrescendo", "User", "Restricted", "GroupPermissionError"]


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


class GroupPermissionError(CheckFailure):
    message: str
    execute: str
    given: PermissionGroup
    required: PermissionGroup

    def __init__(self, given, required, message="", execute=""):
        self.message = message
        self.execute = execute
        self.given = given
        self.required = required

    def make_message(self):
        return self.message if self.message else \
            "{}를 실행하기 위해 필요한 권한이 없습니다. (당신: `{}` < 필요: `{}`)".format(
                self.execute, self.given.name, self.required.name
                ) if self.execute else \
                "당신은 권한이 부족합니다. (당신: `{}` < 필요: `{}`)".format(
                    self.given.name, self.required.name
                    )
