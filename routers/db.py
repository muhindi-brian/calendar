from fastapi import APIRouter, status, HTTPException, Query
from typing import Optional, List


from models import schemas
from db.crud import (
    add_admin, get_admin, get_admins, delete_admin, update_admin
)


router = APIRouter(tags=["Database CRUD"], prefix="/db", include_in_schema=False)


@router.post(
    "/add",
    response_model=schemas.Admins_Pydantic,
    status_code=status.HTTP_202_ACCEPTED,
)
async def add_admin_in_database(admin: schemas.AdminsIn_Pydantic):
    """Add admin to database.

    Args:
        admin (schemas.AdminsIn_Pydantic): admin pydantic object

    Returns:
        admin (AdminsIn_Pydantic): admin object added.
    """
    return await add_admin(admin)


@router.get(
    "/get",
    response_model=schemas.Admins_Pydantic,
    status_code=status.HTTP_202_ACCEPTED
)
async def get_admin_in_database(
    domain: Optional[str] = Query(None),
):
    """Get Admin in database.

    Args:
        domain (Optional[str], optional): workspace domain.
        Defaults to Query(None).

    Returns:
        admin  (AdminsIn_Pydantic): admin object.
    """
    return await get_admin(domain)


@router.get(
    "/all",
    response_model=List[schemas.Admins_Pydantic],
    status_code=status.HTTP_202_ACCEPTED
)
async def get_admins_in_database():
    """Get Admins in database.

    Returns:
        admins: Admin objects from database.
    """
    return await get_admins()


@router.delete(
    "/delete",
    status_code=status.HTTP_202_ACCEPTED
)
async def delete_admin_in_database(
    domain: Optional[str] = Query(None),
):
    """Delete admin in database.

    Args:
        domain (Optional[str], optional): workspace domain.
        Defaults to Query(None).

    Raises:
        HTTPException: if domain is not in database.

    Returns:
        Dict[str, str]: dictionary of status code and message
    """
    if await delete_admin(domain) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Domain {domain} not found."
        )
    return {
        "status": status.HTTP_202_ACCEPTED,
        'message': f"Domain {domain} deleted from database."
    }


@router.put(
    "/update",
    response_model=schemas.Admins_Pydantic,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_admin_in_database(
    admin: schemas.AdminsIn_Pydantic,
    domain: Optional[str] = Query(None)
):
    """Update Admin in database.

    Args:
        admin (schemas.AdminsIn_Pydantic): admin object
        domain (Optional[str], optional): workspace domain.
        Defaults to Query(None).

    Returns:
        admin  (AdminsIn_Pydantic): updated admin object.
    """
    return await update_admin(domain, admin)
