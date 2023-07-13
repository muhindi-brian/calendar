from typing import List, Dict, Optional
from services.setup_services import service_account as sa
from helpers import timer


scopes: Optional[str] = None


@timer.timer
def get_api_responce(email) -> Dict[str, List]:
    """Obtains Users and their primary emails.\n

    Args:
        email ([type]): email of the administrator to enterprise domain.

    Returns:
        Dict[str, List]: Dictionary of user object.
    """
    directory_api_service_account = sa(
        scopes=scopes,
        serviceName="admin",
        version="directory_v1",
        credentials="service_account_key.json",
        email=email,
    )
    domain = email.split('@')[1]
    print(f"+++Getting the users in the {domain}+++\n")
    return (
            directory_api_service_account.users()
            .list(
                customer="my_customer",
                orderBy="email",
            )
            .execute()
        )


@timer.timer
def get_user_emails(email: str, admin_email: str) -> List[Dict[str, str]]:
    """Gets dictionary of user names and emails in domain.

    Args:
        email (str): Email of user to impersonate.
        admin_email (str): Email of domain super admin.

    Returns:
        List[Dict[str, str]]: Dictionary with user name and email
    """
    results = get_api_responce(admin_email)
    users = results.get("users", [])

    if not users:
        domain = email.split('@')[1]
        print(f"+++++++No users in the {domain}+++++++")
    else:
        print("++++++++++++Users found++++++++++++++\n")
        users_object = []
        for user in users:
            name = f"{user['name']['fullName']}"
            email = f'{user["primaryEmail"]}'
            try:
                photo = f'{user["thumbnailPhotoUrl"]}'
            except KeyError:
                photo = None
            domain_user = {"name": name, "email": email, "photo": photo}
            users_object.append(domain_user)
    return users_object
