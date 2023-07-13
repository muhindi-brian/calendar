from models.schemas import AdminsIn_Pydantic, Admins_Pydantic
from models.models import SuperUsers as Admins
from helpers.timer import timer


@timer
async def add_admin(admin: AdminsIn_Pydantic):
    """Add admin in database.

    Args:
        admin (AdminsIn_Pydantic): admin object to be added.
    Returns:
        admin (AdminsIn_Pydantic): admin object added.
    """
    admin_obj = await Admins.create(**admin.dict(exclude_unset=True))
    return await Admins_Pydantic.from_tortoise_orm(admin_obj)


@timer
async def get_admin(domain: str) -> Admins_Pydantic:
    """Gets admin in database.

    Args:
        domain (str): domain to obtain admin for

    Returns:
        admin  (AdminsIn_Pydantic): admin object.
    """
    return await Admins_Pydantic.from_queryset_single(
        Admins.get(domain=domain)
    )


@timer
async def get_admins():
    """Get admins in database

    Returns:
        admins: Admin objects from database.
    """
    return await Admins_Pydantic.from_queryset(Admins.all())


@timer
async def update_admin(domain: str, admin: AdminsIn_Pydantic):
    """Update admin in database

    Args:
        domain (str): domain to update admin.
        admin (AdminsIn_Pydantic): Admin updates.

    Returns:
        admin  (AdminsIn_Pydantic): updated admin object.
    """
    await Admins.filter(domain=domain).update(
        **admin.dict(exclude_unset=True)
    )
    return await Admins_Pydantic.from_queryset_single(
        Admins.get(domain=domain)
    )


@timer
async def delete_admin(domain: str):
    """Delete admin for given domain in database.

    Args:
        domain (str): domain for admin to delete.

    Returns:
        admin  (AdminsIn_Pydantic): deleted admin object.
    """
    admin = await Admins.filter(domain=domain).delete()
    if not admin:
        return None
    return admin
