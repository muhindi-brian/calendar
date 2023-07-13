import inspect
from pydantic import BaseModel
from datetime import datetime
from fastapi import Form
from typing import List, Dict, Optional, Type
from tortoise.contrib.pydantic import pydantic_model_creator
from models import models
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        if not model_field.required:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(model_field.default),
                    annotation=model_field.outer_type_,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls


class UserBase(BaseModel):
    email: str


class DomainUser(UserBase):
    name: str
    photo: str


class OpenSlot(BaseModel):
    start: datetime
    end: datetime


class EventCreate(BaseModel):
    attendee_email: str
    title: str
    description: str
    start: datetime
    end: datetime
    timezone: str
    reminder: Optional[bool] = True
    drive_file: Optional[Dict[str, str]] = None
    other_attendees: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "attendee_email": "gideon@businesscom.africa",
                "title": "Title of event",
                "description": "Brief description of event",
                "start": datetime.now(),
                "end": datetime.now(),
                "timezone": "Africa/Nairobi",
                "reminder": True,
                "drive_file": {
                    "name": "Demo file",
                    "url": "https://docs.google.com/document/d/14hOityW6-pS2l3GBkcFDF1Lcu9HdZk38zAGnloMTy90/edit?usp=sharing",
                    "mime_type": "application/vnd.google-apps.document",
                    "icon_url": "https://drive-thirdparty.googleusercontent.com/16/type/application/vnd.google-apps.document",
                },
                "other_attendees": ["example1@mail.com", "example2@mail.com"],
            }
        }


class CreatedEvent(BaseModel):
    Event_link: str
    Time: datetime
    Timezone: str


Admins_Pydantic = pydantic_model_creator(models.SuperUsers, name="Admins")
AdminsIn_Pydantic = pydantic_model_creator(
    models.SuperUsers, name="AdminsIn", exclude_readonly=True
)


@as_form
class FormData(BaseModel):
    timezone: str
    slot: str
    firstname: str
    lastname: str
    company: str
    email: str
    phone: str
    comments: str
    reminder: Optional[bool] = True
    others: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    iconUrl: Optional[str] = None
    mimeType: Optional[str] = None
