import shutil
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

# 저장 위치: 2.structure/static/files (실행 위치와 무관하게 고정)
FILE_DIR = Path(__file__).resolve().parent.parent / "static" / "files"
FILE_DIR.mkdir(parents=True, exist_ok=True)

file_router = APIRouter(tags=["File"])


def safe_path(filename: str) -> Path:
    # "../../.env" 같은 경로 조작 차단: 폴더 부분을 버리고 파일명만 사용
    name = Path(filename.replace("\\", "/")).name
    if name in ("", ".", ".."):
        raise HTTPException(status_code=400, detail="잘못된 파일명입니다.")
    return FILE_DIR / name


# 전체 파일 목록
@file_router.get("")
def list_files() -> list[dict]:
    return [
        {"filename": p.name, "size": p.stat().st_size}
        for p in sorted(FILE_DIR.iterdir())
        if p.is_file()
    ]


# 업로드: 파일 선택 후 전송 (같은 이름이면 덮어씀)
@file_router.post("/upload")
def upload_file(file: UploadFile = File(...)) -> dict:
    path = safe_path(file.filename or "")
    with path.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": path.name, "size": path.stat().st_size}


# 다운로드: 파일명 입력 후 전송
@file_router.get("/download")
def download_file(filename: str) -> FileResponse:
    path = safe_path(filename)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="파일이 없습니다.")
    return FileResponse(path, filename=path.name)
