__all__ = ["Owner", "TeamCrescendo", "User", "Restricted"]


class PermissionGroup:
    name = ""
    rank = ""


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
