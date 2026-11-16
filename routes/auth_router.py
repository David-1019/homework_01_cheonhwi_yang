from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from schemas.auth_schema import UserSignin
from db import auth_db 

auth_router = APIRouter(tags=["실습2"])

@auth_router.post("/signin")
async def signin(email : EmailStr, user : UserSignin) ->UserSignin:
    result = await auth_db.signin(email, user)
    if result == None:
        raise HTTPException(status_code=404, detail="이미 존해하는 회원입니다.")
    return result

@auth_router.post("/login")
async def login(email : EmailStr, password : str, user : UserSignin) ->UserSignin:
    result = await auth_db.login(email, password, user)
    if result == 1:
        raise HTTPException(status_code=404, detail="존재하지 않은 회원 입니다.")
    elif result == 2:
        raise HTTPException(status_code=403, detail="비밀번호가 틀렸습니다.")
    else:
        print(f"인증 성공입니다.{result}")
        return result




