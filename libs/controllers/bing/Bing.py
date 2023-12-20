import uuid
import os
import imghdr
import requests

from requests.exceptions import MissingSchema
from requests import Response
from fastapi import  File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pathlib import Path

from libs.services import Google
from libs.services import Bing
from libs.helpers import BodyResponse

class BingController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.post('/search')(self.__search_image)
        self.router.get('/search')(self.__search_image_by_url)

    async def __search_image(self, image: UploadFile = File(...)) -> JSONResponse:
        image_byte: bytes = image.file.read()
        try:
            format: str = imghdr.what(image.filename, image_byte)
            if(not format): 
                return JSONResponse(content=BodyResponse(HTTPStatus.BAD_REQUEST, None, message='The image format is not correct').__dict__, status_code=HTTPStatus.BAD_REQUEST)
                
            name: str = f'{uuid.uuid4()}.{format}'
            path: Path = Path(f'{os.getcwd()}/{name}')
            with open(str(path), 'wb') as file:
                file.write(image_byte)

            response: dict = Bing().search_by_image(str(path))
            
            path.unlink(missing_ok=True)
            return JSONResponse(content=BodyResponse(HTTPStatus.OK, data=response).__dict__, status_code=HTTPStatus.OK)
        except Exception as e:
            path.unlink(missing_ok=True)
            return JSONResponse(content=BodyResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e)).__dict__, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)            

    async def __search_image_by_url(self, url_image: str = None) -> JSONResponse:
        try:
            response: Response = requests.get(url_image, stream=True)
            if(response.status_code != 200): 
                return JSONResponse(content=BodyResponse(HTTPStatus.NOT_FOUND, None, message='url image not found').__dict__, status_code=HTTPStatus.NOT_FOUND)
            
            format: str = imghdr.what(None, b"".join(response.iter_content(chunk_size=128)))

            if(not format): 
                return JSONResponse(content=BodyResponse(HTTPStatus.BAD_REQUEST, None, message='url not contain image').__dict__, status_code=HTTPStatus.BAD_REQUEST)
            response: dict = Bing().search_by_url(url_image)
            return JSONResponse(content=BodyResponse(HTTPStatus.OK, response).__dict__, status_code=HTTPStatus.OK)
        
        except MissingSchema as e:
            return JSONResponse(content=BodyResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e)).__dict__, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JSONResponse(content=BodyResponse(HTTPStatus.INTERNAL_SERVER_ERROR).__dict__, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

bingController: BingController = BingController()