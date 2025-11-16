from pydantic import BaseModel
from pydantic.networks import NameEmail


class PasswordResetRequestModel(BaseModel):
    email: NameEmail


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
