import uuid
import os
import imghdr

from fastapi import  File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pathlib import Path

from libs.services import Google
from libs.helpers import BodyResponse

router = APIRouter()

@router.post('/search')
async def upload(image: UploadFile = File(...)) -> JSONResponse:
    image_byte: bytes = image.file.read()
    # try:
    format: str = imghdr.what(image.filename, image_byte)

    if(not format): 
        return JSONResponse(content=BodyResponse(HTTPStatus.BAD_REQUEST, None).__dict__, status_code=HTTPStatus.BAD_REQUEST)
        
    name: str = f'{uuid.uuid4()}.{format}'
    path: Path = Path(f'{os.getcwd()}/{name}')

    with open(str(path), 'wb') as file:
        file.write(image_byte)

    response: Google = Google().start(str(path))
    
    path.unlink(missing_ok=True)

    return JSONResponse(content=BodyResponse(HTTPStatus.OK, response['data']).__dict__, status_code=HTTPStatus.OK)
    # except:
    #     return JSONResponse(content=BodyResponse(HTTPStatus.INTERNAL_SERVER_ERROR, None).__dict__, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)