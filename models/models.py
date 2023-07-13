from tortoise.models import Model
from tortoise import fields


# class Admins(Model):
#     """Admins database model.

#     Args:
#         Model (Any): tortoise_orm model.
#     """
#     id = fields.IntField(pk=True, index=True)
#     domain = fields.CharField(max_length=255, unique=True, index=True)
#     name = fields.CharField(max_length=255)
#     email = fields.CharField(max_length=255, unique=True)

class SuperUsers(Model):
    id = fields.IntField(pk=True, index=True)
    domain = fields.CharField(max_length=255, unique=True, index=True)
    name = fields.CharField(max_length=255, unique=False, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    role = fields.CharField(max_length=255, unique=False, index=True)

    class Meta:
        table="super_user"