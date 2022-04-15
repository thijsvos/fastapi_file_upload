from fastapi import FastAPI, Depends, HTTPException, status
from models import FileModel
from sqlmodel import Session, SQLModel
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import create_engine

import base64
import uvicorn
import aiofiles
import os
import ntpath


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SQLITE_CONN_STRING = 'sqlite:///'+os.path.join(BASE_DIR, 'files.db')
AUTH_TOKEN = "DUMMY-API-KEY"
FILE_WRITE_DIRECTORY = f"{BASE_DIR}/results/"
os.makedirs(os.path.dirname(FILE_WRITE_DIRECTORY), exist_ok=True)

engine = create_engine(SQLITE_CONN_STRING, echo=True)
session = Session(bind=engine)

# Add FastAPI(docs_url=None) attribute to disable Swagger documentation on {url}/docs
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


def auth_request(token: str = Depends(oauth2_scheme)) -> bool:
    authenticated = token == os.getenv("API_KEY", AUTH_TOKEN)
    return authenticated


def correct_base64(base64_string: str) -> bool:
    try:
        base64.b64encode(base64.b64decode(base64_string))
        return True
    except Exception as e:
        print(e)
        return False


async def write_file_to_database(file: FileModel):
    session.add(file)
    session.commit()


async def write_file_to_disk(file: FileModel):
    filename = ntpath.basename(file.file_name)
    full_file_path = os.path.join(FILE_WRITE_DIRECTORY, filename)
    async with aiofiles.open(full_file_path, 'wb') as out_file:
        content = base64.b64decode(file.base64_string)
        await out_file.write(content)


@app.post('/files', response_model=FileModel, status_code=status.HTTP_201_CREATED)
async def create_a_file(file: FileModel, authenticated: bool = Depends(auth_request)) -> FileModel:
    if not authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if not correct_base64(file.base64_string):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file/base64 was corrupt.")

    await write_file_to_database(file)
    await write_file_to_disk(file)
    return file


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
