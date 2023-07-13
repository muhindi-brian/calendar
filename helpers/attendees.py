from typing import List, Dict


def sort_attendees(emails: List[str]) -> List[Dict]:
    """
    Sort the list of other event attendees.
    Args:
        emails: list, list of emails
    Returns:
        list, list of email dictionaries.
    """
    return [{"email": f"{email}"} for email in emails]
