from typing import Optional, List

from support.models import StaffUser


def get_stuff_user(
        name: Optional[str] = None,
        email: Optional[str] = None
) -> Optional[StaffUser]:
    if name:
        user = StaffUser.objects.filter(name=name)
    elif email:
        user = StaffUser.objects.filter(email=email)
    else:
        raise AttributeError("`name` or `email` arguments required. Please provide one of them.")

    return user.first()


def get_all(exclude_names: list[str]) -> List[StaffUser]:
    users = StaffUser.objects.all()
    if exclude_names:
        users = users.exclude(name__in=exclude_names)
    return users
