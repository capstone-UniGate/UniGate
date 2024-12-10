from sqlmodel import SQLModel  # type: ignore  # noqa: F401

from unigate.models.auth import AuthUser
from unigate.models.base import (
    AuthUserBase,
    DBAuthBase,
    DBUnigateBase,
    GroupBase,
    UserBase,
    UUIDBase,
)
from unigate.models.group import Group
from unigate.models.join import Join
from unigate.models.request import Request, RequestStatus
from unigate.models.student import Student
from unigate.models.super_student import SuperStudent

__all__ = [
    "AuthUser",
    "AuthUserBase",
    "DBAuthBase",
    "DBUnigateBase",
    "Group",
    "GroupBase",
    "Join",
    "Request",
    "RequestStatus",
    "Student",
    "SuperStudent",
    "UUIDBase",
    "UserBase",
]
