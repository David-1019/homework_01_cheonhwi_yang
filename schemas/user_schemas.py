from pydantic import BaseModel, EmailStr, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username : str
    password : str
    email : EmailStr
    name : str
