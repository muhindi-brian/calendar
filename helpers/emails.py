import re
from typing import Union


def other_attendees(emails: str):
    """
    Sorts comma separated emails into a list.

    Args:
        emails: str, comma separated emails string

    Returns:
        list of emails.
    """
    if emails is not None:
        if "," in emails:
            return emails.split(",")
        return list(emails)


def check(email: str) -> Union[str, None]:
    """Verifies string entered is an email.

    Args:
        email (str): email string

    Returns:
        Union[str, None]: email if verified or None
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return email
    else:
        return None
