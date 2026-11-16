from schemas.user_schemas import User
from sqlalchemy.orm import Session
#orm은 각 데이터 베이스에게 맞게끔 명령어를 통일화 해서 저장해 놓은 모듈~
from models import user_model
from schemas.user_update_schemas import  Userupdate

async def get_users(db : Session) -> list[User]:
    userTable = db.query(user_model.User).all()
    #print("user table: ", userTable)
    if len(userTable) == 0: #not userTable
        return None
    users = [User.model_validate(user) for user in userTable]
    '''
    users = []
    for user in userTable: #userTable = [객체1, 객체2]
        users.append( User.model_validate(user) ) #db모델 -> 스키마 변환
    '''
    return users

async def get_user(email : str, db : Session) -> User | None:
    userTable = (db.query(user_model.User)
                    .filter(user_model.User.email == email)
                    .first()
                    )
    if userTable is None:
        return None
    return User.model_validate(userTable)

async def insert( user : User , db : Session) -> User | None:
    exist_user =  ( 
                    db.query(user_model.User)
                    .filter( user_model.User.username == user.username )
                    .first()
                  )
    if exist_user:
        return None
    userTable = user_model.User( **user.model_dump() )
    print("저장 전 확인 id : ",userTable.id ) #id 없음
    db.add( userTable ) #insert db 임시 저장
    db.commit() #db 완벽히 저장
    db.refresh(userTable) #저장된 정보를 다시 가져옴
    print("저장 후 확인 id : ",userTable.id) #id 존재함

    return user

async def update(username : str, user: Userupdate, db : Session):
    userTable = (db.query(user_model.User)
                    .filter(user_model.User.username == username)
                    .first()
                    )    
    if userTable is None:
        return None 
    #userTable.name = user.name
    #userTable.email = user.email
    user_dict = user.model_dump(exclude_unset= True)
    print("user dict: ", user_dict)

    for k,v in user_dict.items():
        setattr(userTable,k,v) #딕셔너리에 각 속성에 맟춰 넣어라 
    db.commit()
    db.refresh(userTable)
    print("이후: ", userTable)
    return User.model_validate(userTable)
    
async def delete(username : str, db : Session):
    userTable = (db.query(user_model.User)
                    .filter(user_model.User.username == username)
                    .first()
                    )    
    if userTable is None:
        return None
    deleted = User.model_validate(userTable)  # 삭제 후엔 객체를 읽을 수 없어서 먼저 변환
    db.delete(userTable)
    db.commit()
    return deleted
    
async def db_get_one(id : int, db : Session):
    userTable = db.get(user_model.User, id)
    if not userTable:
        return None  
    return User.model_validate(userTable)


