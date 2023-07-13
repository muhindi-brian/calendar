from fastapi import APIRouter, status, HTTPException, Query
from typing import Optional, List
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError, TransportError


from models import schemas
from db.crud import get_admin
from services.get_users import get_user_emails
from services.get_slots import get_open_slots
from services.create_appointment import make_appointment


router = APIRouter(tags=["Calender API"], prefix="/calender")

test_email: Optional[str] = None

reg = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


@router.get(
    "/users",
    response_model=List[schemas.DomainUser],
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_domain_users(
    email: Optional[str] = Query(None, regex=reg),
):
    """Get user for domain in email provided.

    Args:
        email (Optional[str], optional): calender email.
            Defaults to Query(None, regex=reg).

    Raises:
        HTTPException: If RefreshError is true
        HTTPException: If TransportError is true
        HTTPException: If HttpError is true

    Returns:
        List[Dict[str, str]]: Dictionary with user name and email
    """
    try:
        if email is not None:
            admin = await get_admin(
                email.split('@')[1]
            )
            admin_email = dict(admin)['email']
        return (
            get_user_emails(
                email=test_email, admin_email=test_email
                ) if email is None else get_user_emails(
                    email=email, admin_email=admin_email
                )
        )
    except RefreshError as error:
        # Pick up google error and return it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.args[0]
        )
    except TransportError as error:
        # Pick up google error and return it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.args[0]
        )
    except HttpError as error:
        # Pick up google error and return it
        print(error)
        raise HTTPException(
            status_code=error.status_code,
            detail=error.error_details
        )


@router.get(
    "/open",
    response_model=List[schemas.OpenSlot],
    status_code=status.HTTP_202_ACCEPTED
)
def get_appointment(
    email: Optional[str] = Query(None, regex=reg),
):
    """Get Open Appointment slots for a given user.

    Args:
        email (Optional[str], optional): calender email.
            Defaults to Query(None, regex=reg).

    Raises:
        HTTPException: If RefreshError is true
        HTTPException: If TransportError is true
        HTTPException: If HttpError is true

    Returns:
        List[Dict[str, str]]: list of dictionaries with
            appointment datetime slots.
    """
    try:
        return (
            get_open_slots(
                email=test_email
            ) if email is None else get_open_slots(email=email)
        )
    except RefreshError as error:
        # Pick up google error and return it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.args[0]
        )
    except TransportError as error:
        # Pick up google error and return it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.args[0]
        )
    except HttpError as error:
        # Pick up google error and return it
        print(error)
        raise HTTPException(
            status_code=error.status_code,
            detail=error.error_details
        )


@router.post(
    "/make",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreatedEvent
)
def create_event(
    event: schemas.EventCreate,
    email: Optional[str] = Query(None, regex=reg),
):
    """
    Book an Appointment.

    Args:
        event (schemas.EventCreate): calender event pydantic object
        email (Optional[str], optional): calender email.
            Defaults to Query(None, regex=reg).

    Raises:
        HTTPException: If HttpError is true
        HTTPException: If TransportError is true

    Returns:
        Dict[str, str]: Link to calender event and additional details.
    """
    try:
        return make_appointment(email=email, event=event)
    except HttpError as error:
        # Pick up googleapiclient error and return it
        raise HTTPException(
            status_code=error.status_code,
            detail=error.error_details
        )
    except TransportError as error:
        # Pick up google error and return it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.args[0]
        )
