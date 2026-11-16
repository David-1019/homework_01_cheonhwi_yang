from pydantic import EmailStr
from schemas.auth_schema import UserSignin

users : list[UserSignin] = [
    UserSignin(email="aaa@aaa.aaa", password="aaa"),
    UserSignin(email="bbb@bbb.bbb", password="aaa")
]

async def signin(email : EmailStr, user : UserSignin) -> UserSignin | None:
    for i in users:
        if i.email == email:
            return None
    users.append(user)
    return user

async def login(email : EmailStr, password : str, user : UserSignin) -> UserSignin | int:
    for i in users:
        if i.email == email:          # 이메일이 같은 회원을 찾았을 때만 비밀번호 비교
            if i.password != password:
                return 2
            return i
    return 1                          # 끝까지 못 찾으면 없는 회원
