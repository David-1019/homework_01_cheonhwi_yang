import os
import uvicorn
from fastapi import FastAPI
from routes.user_routes import user_router
from routes.auth_router import auth_router
from routes.file_router import file_router

from contextlib import asynccontextmanager

from models import user_model  # create_all에 users 테이블을 등록하려면 필요 (지우지 말 것)
from db.connection import Base, engine

from fastapi import Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 서버 시작 시 설정 내용 ---")
    #print(Base.metadata.tables)
    if os.getenv("SKIP_DB_INIT") != "1":  # 로컬에서 DB 없이 Docs만 볼 때 .env에 SKIP_DB_INIT=1
        Base.metadata.create_all(bind=engine)
    yield
    print("--- 서버 종료 시 설정 내용 ---")

app = FastAPI(lifespan=lifespan)

app.include_router( user_router , prefix="/users")
app.include_router( auth_router , prefix="/auth")
app.include_router( file_router , prefix="/files")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], # [http://localhost:3000, 등등]               
    allow_methods=["*"], # http 통신 방식 (get, put, post, delete)
    allow_headers=["*"]) # [http 통신헤더 받을 지]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
    #http://localhost:8000/docs


@app.get("/")
async def index(request: Request) -> dict:
    return {
    "index": "success",
    "ec2-ip": request.client.host,
    }