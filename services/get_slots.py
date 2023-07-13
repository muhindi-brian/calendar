from datetime import datetime, timedelta, time
from typing import Optional, Dict, List
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


# from models.config import SCOPES as scopes
from services.setup_services import service_account as sa
from helpers.timer import timer

scopes: Optional[str] = None


@timer
def freebusy_slots(email: str) -> Dict:
    """Get freebusy slots for user with email.

    Args:
        email (str): email of user to impersonate with service account.

    Returns:
        Dict: [description]
    """
    now = (
        datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    )  # 'Z' indicates UTC time zulu
    month_later = (
        datetime.utcnow().replace(microsecond=0) + timedelta(days=30)
    ).isoformat() + "Z"
    query = {
        "timeMin": now,
        "timeMax": month_later,
        "timeZone": "UTC",
        "calendarExpansionMax": 100,
        "groupExpansionMax": 50,
        "items": [{"id": "primary"}],
    }
    impersonated_user_service = sa(
        scopes=scopes,
        serviceName="calendar",
        version="v3",
        credentials="service_account_key.json",
        email=email,
    )

    return impersonated_user_service.freebusy().query(body=query).execute()


@timer
def get_open_slots(email: str) -> List[Dict[str, str]]:
    """Obtains open Appointment slots for user with email.

    Args:
        email (str): email of user to abotain open calender slots.

    Returns:
        List[Dict[str, str]]: list of dictionaries with
        appointment datetime slots.
    """
    # Range to search for open times in.
    start_time = datetime.utcnow().replace(
        microsecond=0, tzinfo=ZoneInfo("UTC")
    )
    end_time = start_time + timedelta(days=30)

    # Kick off first appointment time at beginning of the day.
    if start_time.time() < time(hour=5):
        appt_start_time = start_time.replace(hour=5, minute=00, second=00)
    else:
        appt_start_time = start_time

    # Loop through each appointment slot in the search range.
    open_slots = []
    freebusy_sa_result = freebusy_slots(email)
    while appt_start_time < end_time:
        # Add 29:59 to the appointment start time
        # so we know where the appointment will end.
        appt_end_time = appt_start_time + timedelta(minutes=29, seconds=59)

        # For each appointment slot, loop through the current appointments
        # to see if it falls in a slot that is already taken.
        slot_available = True
        for appt_slot in freebusy_sa_result["calendars"]["primary"]["busy"]:
            event_start = datetime.strptime(
                appt_slot["start"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=ZoneInfo("UTC"))
            event_end = datetime.strptime(
                appt_slot["end"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=ZoneInfo("UTC"))

            # If the appointment start time or appointment end time falls
            # on a current appointment, slot is taken.
            if (
                appt_start_time >= event_start and appt_start_time < event_end
            ) or (
                appt_end_time >= event_start and appt_end_time < event_end
            ):
                slot_available = False
                # No need to continue if it's taken.
                break

        # If we made it through all appointments and the slot is still
        # available, it's an open slot.
        if (
            slot_available
            and (  # Check if appointment time is btw 8am EAT and 5pm EAT
                appt_start_time.time()
                >= datetime.strptime("05:00:00", "%H:%M:%S").time()
                and appt_start_time.time()
                < datetime.strptime("13:30:59", "%H:%M:%S").time()
            )
            and appt_start_time.date().weekday() < 5
        ):
            # Save open slots btw working hrs and days.
            event_slot = {
                "start": appt_start_time,
                "end": appt_end_time,
            }
            open_slots.append(event_slot)

        # Check if appointment day has changed
        if (
            appt_start_time.time() > time(hour=00) and
            appt_start_time.time() < time(hour=1)
        ):
            # Set appointment start time to 8AM
            appt_start_time = appt_start_time.replace(
                hour=5, minute=0, second=0
            )
        else:
            # + 30 minutes and additional 10 min allowance for event extension
            appt_start_time += timedelta(minutes=40)
    return open_slots
