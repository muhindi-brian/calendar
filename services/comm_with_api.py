from fastapi import status, HTTPException, Query
from typing import Optional, Dict, List
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError, TransportError
from rich import print

from models import schemas
from services.get_users import get_user_emails
from services.get_slots import get_open_slots
from services.create_appointment import make_appointment
from helpers.timer import timer


@timer
def get_user_info(email: str, admin_email: str) -> Dict[str, str]:
    """Get user information based on email in route extension.

    Args:
        email (str): email of user to access calender
        admin_email (str): Email of domain super admin.

    Returns:
        Dict[str, str]: workspace user object.
    """
    try:
        domain = email.split("@")[1]
    except IndexError as err:
        print(err)
        domain = None
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(domain)
    # send domain name to Calender API to help determine
    #  which service account credentials to use.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    try:
        users = get_user_emails(email, admin_email)
    except (RefreshError, TransportError) as error:
        # Pick up google error and return it
        print(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error.args[0]
        )
    except HttpError as error:
        print(error)
        # Pick up google error and return it
        raise HTTPException(status_code=error.status_code, detail=error.error_details)
    else:
        for user in users:
            if email == user["email"]:
                return user


test_email: Optional[str] = None

reg = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


@timer
def get_appointment(
    user_email: Optional[str] = Query(None, regex=reg),
) -> List[Dict[str, str]]:
    """Get Open Appointment slots for a given user.

    Args:
        user_email (Optional[str], optional): email for calender
        to book appointment on. Defaults to Query(None, regex=reg).

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [list]: list of open slots in calender
    """
    try:
        return (
            get_open_slots(email=test_email)
            if user_email is None
            else get_open_slots(email=user_email)
        )
    except (RefreshError, TransportError) as error:
        print(error)
        # Pick up google error and return it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error.args[0]
        )
    except HttpError as error:
        print(error)
        # Pick up google error and return it
        raise HTTPException(status_code=error.status_code, detail=error.args[0])


@timer
def slots(email: str) -> List[Dict[str, str]]:
    """Gets open calender slots for impersonated user

    Args:
        email (str): email of calender to add event.

    Returns:
        List[Dict[str, str]]: list of open slots
    """
    return get_appointment(user_email=email)


@timer
def create_event(
    event: schemas.EventCreate,
    email: Optional[str] = Query(None, regex=reg),
) -> Dict[str, str]:
    """Book an Appointment.

    Args:
        event (schemas.EventCreate): Calender Event object.
        email (Optional[str], optional): calender email.
        Defaults to Query(None, regex=reg).

    Raises:
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        Dict[str, str]: Link to calender event and additional details.
    """
    try:
        return make_appointment(email=email, event=event)
    except HttpError as error:
        print(error)
        # Pick up googleapiclient error and return it
        raise HTTPException(status_code=error.status_code, detail=error.error_details)
    except (RefreshError, TransportError) as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error.args[0]
        )
