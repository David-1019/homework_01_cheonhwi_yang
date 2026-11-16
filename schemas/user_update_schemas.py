from pydantic import BaseModel, EmailStr


class Userupdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None