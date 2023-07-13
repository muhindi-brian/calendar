import os.path

from typing import List
from helpers.timer import timer

from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account as sa


@timer
def service(
    scopes: List[str], serviceName: str, version: str, credentials: str
) -> Resource:
    """Construct a Service Resource for interacting
    with an API.
    Construct a Resource object for interacting with an API. 
    The serviceName and version are the names from the Discovery service.

    Args:
        scopes (List[str]): list of scopes implemented.
        serviceName (str): name of the service.
        version (str): the version of the service.
        credentials (str): the path to json secret file

    Returns:
        Resource: [description]
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path="token.json"):
        creds = Credentials.from_authorized_user_file(
            filename="token.json", scopes=scopes
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file=credentials, scopes=scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(file="token.json", mode="w") as token:
            token.write(creds.to_json())

    return build(serviceName=serviceName, version=version, credentials=creds)


@timer
def service_account(
    scopes: List[str], serviceName: str,
    version: str, credentials: str,
    email: str
) -> Resource:
    """Construct a Service Resource for interacting with an API.
    Construct a Resource object for interacting with an API.
    The serviceName and version are the names from the Discovery service.

    Args:
        scopes (List[str]): list of scopes implemented.
        serviceName (str): name of the API service.
        version (str): the version of the API service.
        credentials (str): the path to json secret file downloaded after\
            setting up service account.
        email (str): email of user to impersonate

    Returns:
        Resource: Service Account Resource Object
    """
    creds = sa.Credentials.from_service_account_file(
        filename=credentials, scopes=scopes
    )
    delegate_cred = creds.with_subject(subject=email)

    return build(
        serviceName=serviceName, version=version, credentials=delegate_cred
    )
