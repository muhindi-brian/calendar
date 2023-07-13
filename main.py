import yaml
import sentry_sdk
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from services import create_appointment, get_slots, get_users
from views import home
from routers import calender, db


# sentry_sdk.init(
#     "https://d26d57773f05410195ed54c7f367b1df@o932539.ingest.sentry.io/5882335",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
# )

app = FastAPI(title="Calender Schedule App")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/schedule")


def configure():
    """
    Configure App.
    """
    print("~~IzZlE~~")
    configure_routing()
    configure_api_creds()
    configure_scopes()
    configure_db()
    print("Running Calender App.")


def configure_routing():
    """
    Configure the Paths to the various services needed by app.
    """
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home.router)
    app.include_router(calender.router)
    app.include_router(db.router)


def configure_api_creds():
    """
    Checks if Credential files are available.
    """
    file = Path("service_account_key2.json").absolute()
    if not file.exists():
        print(
            f"WARNING: {file} file not found, \
                service account file needed to run."
        )
        raise Exception(
            'WARNING: Service account credentials "service_account_key.json" \
                file not found, service account file needed to run.'
        )


def configure_scopes():
    """
    Obtain scopes to run workspace APIs
    """
    file = Path("settings.yaml").absolute()
    if not file.exists():
        print(
            f"WARNING: {file} file not found, you cannot continue, \
                please see settings.yaml"
        )
        raise Exception(
            "settings.yaml file not found, you cannot continue, \
                please see settings.yaml"
        )

    with open("settings.yaml", "r") as conf:
        settings = yaml.safe_load(conf)

        scopes = settings.get("SCOPES")
        create_appointment.scopes = scopes
        get_slots.scopes = scopes
        get_users.scopes = scopes

        test_email = settings.get("EMAILS")[0]
        home.test_email = test_email
        calender.test_email = test_email


def configure_db():
    """
    Setup connection to database.
    """
    with open("settings.yaml", "r") as conf:
        settings = yaml.safe_load(conf)
        db = settings.get("DATABASE")

        register_tortoise(
            app=app,
            # db_url="sqlite://db/admin.db",
            db_url=f"postgres://{db['USERNAME']}:{db['PASSWORD']}@{db['HOST']}/{db['DB']}",
            modules={"models": ["models.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
        )


configure()
