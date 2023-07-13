try:
    import zoneinfo
    from zoneinfo import ZoneInfo
except ImportError:
    from backports import zoneinfo
    from backports.zoneinfo import ZoneInfo
from datetime import datetime
from calendar import Calendar
from typing import List, Dict
from collections import deque


from helpers.timer import timer


timezones = zoneinfo.available_timezones()


@timer
def month_date(dates: List[Dict[str, datetime]]) -> datetime.date:
    """Generates date from today, for the next 30days.

    Args:
        dates (List[Dict[str, datetime]]): list of available
        calender slot dates

    Returns:
        datetime.date: date objects.

    Yields:
        Iterator[datetime.date]: date objects
    """
    # From calender get calender object
    calender = Calendar(firstweekday=6)
    # Get current month
    month = datetime.today().isoformat().split("-")[1]
    month_number = month if month[0] != 0 else month[1]
    # Get list of dates for days in month
    current_month_days = calender.itermonthdates(2021, int(month_number))
    next_month_days = calender.itermonthdates(2021, (int(month_number) + 1))
    dates_for_events = [
        date for date in current_month_days if date >= datetime.now().date()
    ]
    dates_for_events.extend(
        [
            date
            for date in next_month_days
            if date > dates_for_events[-1]
            and date <= dates[-1]["start"].date()
        ]
    )
    queue = deque(dates_for_events)
    # Get dates for 30 days from today
    while queue:
        yield queue.popleft()


@timer
def sorter(
    timezone: str, dates: List[Dict[str, datetime]]
) -> Dict[str, List[str]]:
    """Sort datetime objects into dictionary separating timeslots with same date.

    Args:
        timezone (str): time zone.
        dates (List[Dict[str, datetime]]): List of dictionaries
        of datetime objects

    Returns:
        Dict[str, List[str]]: date object as key with timeslots as values

    Yields:
        Iterator[Dict[str, List[str]]]: date object as key with timeslots as values
    """
    # For date from calender look for matching date in datetime objects
    for date in month_date(dates):
        date_timeslots = {}
        timeslots = []

        # Loop through open slot's datetime strings and getting start time
        for date_dict in dates:
            event_start = date_dict["start"]

            # Check if start datetime object share same date
            if event_start.date() == date:
                name = date.ctime().split(" 00")[0]
                # Localize unaware start timezone
                event_start = event_start.replace(tzinfo=ZoneInfo("UTC"))
                # Save aware time with updated time zone slots in list
                timeslots.append(
                    datetime.strftime(
                        event_start.astimezone(ZoneInfo(timezone)), "%I:%M %p"
                    )
                )
                # save timeslots for matching datetime objects
                # in dict with date as key
                date_timeslots[name] = timeslots
        if date_timeslots:
            # generate dict with date as key and
            # list of event timestamp as values
            yield date_timeslots


@timer
def format_input_time(time: str) -> datetime:
    """Converts time into datetime object with year, month, day, time.\n

    Args:
        time (str): time string object.

    Returns:
        datetime: date time object.
    """
    start_date = datetime.strptime(time, "%a %b %dT%I:%M %p")
    # Compute years to fix year error after conversion
    years = int(datetime.strftime(datetime.now(), "%Y")) - 1900
    # Replacing default year to current
    return start_date.replace(start_date.year + years)


@timer
def format_response_time(date_time: str, zone: str) -> Dict[str, str]:
    """Converts datetime string into a dictionary of formated time and date.

    Args:
        date_time (str): datetime string object (2021-05-27T12:31:00+03:00)
        zone (str): timezone location

    Returns:
        Dict[str, str]: formated time and date.
    """
    new_date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z")

    return {
        "time": datetime.strftime(
            new_date_time.astimezone(ZoneInfo(zone)), "%I:%M %p"
        ),
        "date": datetime.strftime(
            new_date_time.astimezone(ZoneInfo(zone)), "%a, %b %d"
        ),
    }
