from pydantic import BaseModel, EmailStr

class UserSignin(BaseModel):
    email : EmailStr | None = None
    password : str | None = None