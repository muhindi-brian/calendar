from datetime import datetime
from typing import Optional, Dict
from rich import print


from services.setup_services import service_account as sa
from models import schemas
from helpers.attendees import sort_attendees
from helpers.timer import timer


scopes: Optional[str] = None


@timer
def make_appointment(email: str, event: schemas.EventCreate) -> Dict[str, str]:
    """Create a calender event

    Args:
        email (str): email of calender to add event.
        event (schemas.EventCreate): calender event pydantic object.

    Raises:
        error: [description]

    Returns:
        Dict[str, str]: Link to calender event and additional details.
    """
    query = {
        "summary": event["title"],
        "description": event["title"],
        "start": {
            "dateTime": datetime.strptime(
                event["start"], "%Y-%m-%dT%H:%M:%S"
            ).isoformat(),
            "timeZone": event["timezone"],
        },
        "end": {
            "dateTime": datetime.strptime(
                event["end"], "%Y-%m-%dT%H:%M:%S"
            ).isoformat(),
            "timeZone": event["timezone"],
        },
        "attendees": [
            {
                # "displayName": "Gideon Mandu",
                "email": event["attendee_email"],
                "organizer": True,
                "responseStatus": "accepted",
                "comment": event["description"],
            },
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 60},
                {"method": "popup", "minutes": 10},
            ],
        },
        # "location": "800 Howard St., San Francisco, CA 94103",
        # "recurrence": ["RULE:FREQ=DAILY;COUNT=2"],
    }
    # Adding file
    try:
        file = event["drive_file"]
    except KeyError as e:
        print(f"No drive file Added. \n{e}")
    else:
        try:
            query["attachments"] = [
                {
                    "fileUrl": file["url"],
                    "title": file["name"],
                    "mimeType": file["mime_type"],
                    "iconLink": file["icon_url"],
                },
            ]
        except AttributeError as error:
            raise error
    finally:
        # Adding other attendees
        try:
            query["attendees"].extend(sort_attendees(event["other_attendees"]))
        except KeyError:
            print("No additional attendees added.")
        finally:
            impersonated_user_service = sa(
                scopes=scopes,
                serviceName="calendar",
                version="v3",
                credentials="service_account_key.json",
                email=email,
            )

            event = (
                impersonated_user_service.events()
                .insert(
                    calendarId="primary",
                    body=query,
                    supportsAttachments=True,
                )
                .execute()
            )

            return {
                "Event_link": event.get("htmlLink"),
                "Time": event.get("start")["dateTime"],
                "Timezone": event.get("start")["timeZone"],
            }
