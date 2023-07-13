from fastapi import APIRouter, Form, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from datetime import timedelta
from rich import print
from tortoise.exceptions import DoesNotExist

from services import time_dates, comm_with_api
from helpers import emails
from db.crud import get_admin
from models.schemas import FormData


# Setup path to HTML templates files
templates = Jinja2Templates("templates")

# Setup router path for home page.
router = APIRouter(
    tags=["Calender frontend"], prefix="/schedule", include_in_schema=False
)


@router.get("/{calender_email}")
async def timezone(calender_email: str, request: Request):
    calender_email = emails.check(calender_email)
    if calender_email:
        try:
            try:
                admin = await get_admin(calender_email.split("@")[1])
            except DoesNotExist:
                return RedirectResponse("/schedule")
        except IndexError as e:
            print(e)
            return RedirectResponse("/schedule")
        else:
            calender_owner = comm_with_api.get_user_info(
                email=calender_email, admin_email=admin.email
            )
            # handling invalid domain email
            if calender_owner is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{calender_email} is not a valid email.",
                )
            data = {
                "request": request,
                "timezones": sorted(time_dates.timezones),
                "calender_name": calender_owner["name"],
                "calender_email": calender_email,
                "calender_photo": calender_owner["photo"],
            }
            return templates.TemplateResponse("home/timezone.html", data)
    return RedirectResponse("/schedule")


@router.post("/{calender_email}")
async def index(calender_email: str, request: Request, timezone: str = Form(any)):
    # save dates with list of open timeslots in list
    admin = await get_admin(calender_email.split("@")[1])
    try:
        calender_name = comm_with_api.get_user_info(
            email=calender_email, admin_email=admin.email
        )["name"]
    except TypeError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    else:
        dates = [
            date
            for date in time_dates.sorter(
                timezone=timezone, dates=comm_with_api.slots(email=calender_email)
            )
        ]
        data = {
            "request": request,
            "dates": dates,
            "timezone": timezone,
            "calender_name": calender_name,  # "Calender Name"
            "calender_email": calender_email,
            "display": ["d-none", "d-block"],
            "booked_date": None,
            "booked_time": None,
            "link": None,
            "disabled": "",
        }
        return templates.TemplateResponse("home/index.html", data)


@router.post("/booked/{calender_email}")
async def form(
    calender_email: str,
    request: Request,
    form: FormData = Depends(FormData.as_form),
):
    start_datetime = time_dates.format_input_time(form.slot)
    other_attendees = emails.other_attendees(form.others)
    event = {
        "attendee_email": form.email,
        "title": f"{form.firstname} {form.lastname} from {form.company} .",
        "description": f"Comments: {form.comments}.\nPhone no:{form.phone}",
        "start": start_datetime.isoformat(),
        "end": (start_datetime + timedelta(minutes=29, seconds=59)).isoformat(),
        "timezone": form.timezone,
        "reminder": form.reminder,
    }

    if form.others:
        # Add other attendees.
        event["other_attendees"] = other_attendees

    if form.url:
        # Add drive file shared by user.
        event["drive_file"] = {
            "name": form.name,
            "url": form.url,
            "mime_type": form.mimeType,
            "icon_url": form.iconUrl,
        }

    api_response = comm_with_api.create_event(event=event, email=calender_email)
    print(api_response)
    dates = [
        date
        for date in time_dates.sorter(
            timezone=form.timezone, dates=comm_with_api.slots(email=calender_email)
        )
    ]
    date_time = time_dates.format_response_time(
        date_time=api_response["Time"], zone=api_response["Timezone"]
    )
    data = {
        "request": request,
        "dates": dates,
        "timezone": api_response["Timezone"],
        # "calender_name": calender_name,
        "calender_email": calender_email,
        "link": api_response["Event_link"],
        "display": ["d-block", "d-none"],
        "booked_date": date_time["date"],
        "booked_time": date_time["time"],
        "disabled": "disabled",
    }


@router.get("/")
async def error_handler(request: Request):
    return templates.TemplateResponse("home/404.html", {"request": request})
