from fastapi import APIRouter, HTTPException, status
from schemas.user_schemas import User
from db import user_db
from fastapi import Depends, Form
from sqlalchemy.orm import Session
from db.connection import get_db
import time
from db.user_db import db_get_one
from schemas.user_update_schemas import  Userupdate

user_router = APIRouter(tags=["User"])
#라우터 테스트
@user_router.get("/test")
async def test() -> dict:
    db = get_db()
    print("db: ", db)
    print("db: ", next(db))
    time.sleep(3)
    return {"msg": "test"}
#
@user_router.get("/test2")
async def test2(db : Session = Depends(get_db)) -> dict:
    print("db: ", db)
    time.sleep(3)
    return {"msg": "test"}

@user_router.get("/")
async def get_users(db : Session = Depends(get_db))-> list[User]| None:
    users = await user_db.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="값이 없습니다.")
    return users

@user_router.get("/{email}")
async def get_user(email : str, db : Session = Depends(get_db))-> User:
    user = await user_db.get_user(email, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="존재하는 사용자가 없습니다.")

#데이터 추가
@user_router.post("/",response_model=User,status_code=201, summary="회원 가입 입니다.", responses={409 : {"description" : "중복ID"}})
async def post_user(user : User, db : Session = Depends(get_db)):
    result = await user_db.insert(user,db) 
    if result == None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="이미 있는 계정입니다.")
    
    return result 

#데이터 추가 업데이트
@user_router.put("/form/{username}")
async def upadte_user(username : str, user : Userupdate = Form(), db : Session = Depends(get_db)):
    result = await user_db.update(username, user, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="수정 사용자 없음")

@user_router.delete("/{username}")
async def delete (username : str, db : Session = Depends(get_db)) ->User:
    result = await user_db.delete(username, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자 없음")


@user_router.get("/one/{id}")
async def get_user_one(id:int, db:Session = Depends(get_db)):
    result = await db_get_one(id, db)
    if result:
        return result
    raise HTTPException( status_code=404, detail="존재하지 않는 사람입니다.")

@user_router.put("/update/{username}")
async def upadte_user1(username : str, user : Userupdate, db  : Session = Depends(get_db)):
    result = await user_db.update(username, user, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="수정 사용자 없음")
